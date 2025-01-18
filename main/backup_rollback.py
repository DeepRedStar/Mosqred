import os
import shutil
from logging_config import setup_logger

# Set up logger
logger = setup_logger('backup_rollback', 'backup_rollback.log')

def create_backup():
    """Create a backup directory to save original configurations."""
    backup_dir = "backup"
    try:
        if os.path.exists(backup_dir):
            logger.info(f"Backup directory '{backup_dir}' already exists. Removing old backup.")
            shutil.rmtree(backup_dir)
        os.makedirs(backup_dir)
        logger.info(f"Backup directory '{backup_dir}' created.")

        # Backup Mosquitto and Node-RED configurations if they exist
        mosquitto_conf = "/etc/mosquitto/conf.d/default.conf"
        node_red_conf = os.path.expanduser("~/.node-red/settings.js")

        if os.path.exists(mosquitto_conf):
            shutil.copy(mosquitto_conf, backup_dir)
            logger.info(f"Backed up: {mosquitto_conf}")

        if os.path.exists(node_red_conf):
            shutil.copy(node_red_conf, backup_dir)
            logger.info(f"Backed up: {node_red_conf}")
    except Exception as e:
        logger.error(f"Failed to create backup: {e}")
        raise

def rollback_changes():
    """Restore configurations from the backup directory if setup fails."""
    backup_dir = "backup"
    try:
        if os.path.exists(backup_dir):
            mosquitto_conf = os.path.join(backup_dir, "default.conf")
            node_red_conf = os.path.join(backup_dir, "settings.js")

            if os.path.exists(mosquitto_conf):
                shutil.copy(mosquitto_conf, "/etc/mosquitto/conf.d/default.conf")
                logger.info(f"Restored: {mosquitto_conf}")

            if os.path.exists(node_red_conf):
                shutil.copy(node_red_conf, os.path.expanduser("~/.node-red/settings.js"))
                logger.info(f"Restored: {node_red_conf}")

            logger.info("Rollback completed successfully.")
        else:
            logger.warning("No backup directory found. Nothing to roll back.")
    except Exception as e:
        logger.error(f"Failed to roll back changes: {e}")
        raise

if __name__ == "__main__":
    # Test functions
    logger.info("Testing create_backup function.")
    create_backup()
    logger.info("Testing rollback_changes function.")
    rollback_changes()
