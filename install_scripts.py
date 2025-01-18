import os
import subprocess
import shutil
from utils import generate_random_password
from logging_config import setup_logger

# Set up logger
logger = setup_logger('install_scripts', 'install_scripts.log')

def install_mosquitto(mode):
    """Install Mosquitto MQTT broker and configure it for secure communication."""
    try:
        logger.info("Starting Mosquitto installation.")
        if shutil.which("mosquitto"):
            logger.info("Mosquitto is already installed.")
        else:
            subprocess.run(["sudo", "apt-get", "update"], check=True)
            subprocess.run(["sudo", "apt-get", "install", "-y", "mosquitto", "mosquitto-clients"], check=True)
            logger.info("Mosquitto installed successfully.")

        config_path = "/etc/mosquitto/conf.d/default.conf"
        cert_dir = "certs"
        os.makedirs(cert_dir, exist_ok=True)

        mqtt_password = generate_random_password()
        password_file = os.path.join(cert_dir, "mqtt_password.txt")

        with open(password_file, "w") as pw_file:
            pw_file.write(f"admin:{mqtt_password}\n")
        os.chmod(password_file, 0o600)
        logger.info(f"Password file created and secured at {password_file}.")

        with open(config_path, "w") as config_file:
            config_file.write(f"""
listener 8883
cafile {os.path.join(cert_dir, 'ca.crt')}
certfile {os.path.join(cert_dir, 'server.crt')}
keyfile {os.path.join(cert_dir, 'server.key')}
require_certificate true
auth_plugin /usr/lib/mosquitto/auth-plug.so
password_file {password_file}
""".strip())
        os.chmod(config_path, 0o600)
        logger.info(f"Mosquitto configuration file written and secured at {config_path}.")

        subprocess.run(["sudo", "systemctl", "restart", "mosquitto"], check=True)
        logger.info("Mosquitto service restarted successfully.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error installing or configuring Mosquitto: {e}")
        raise

def install_node_red():
    """Install Node-RED and configure it for secure communication."""
    try:
        logger.info("Starting Node-RED installation.")
        if shutil.which("node-red"):
            logger.info("Node-RED is already installed.")
        else:
            subprocess.run(["sudo", "apt-get", "update"], check=True)
            subprocess.run(["sudo", "apt-get", "install", "-y", "npm"], check=True)
            subprocess.run(["sudo", "npm", "install", "-g", "--unsafe-perm", "node-red"], check=True)
            logger.info("Node-RED installed successfully.")

        settings_path = os.path.expanduser("~/.node-red/settings.js")
        cert_dir = "certs"
        os.makedirs(cert_dir, exist_ok=True)

        with open(settings_path, "w") as settings_file:
            settings_file.write(f"""
module.exports = {{
    https: {{
        key: require('fs').readFileSync('{os.path.join(cert_dir, 'server.key')}'),
        cert: require('fs').readFileSync('{os.path.join(cert_dir, 'server.crt')}')
    }},
    mqttReconnectTime: 15000
}};
""".strip())
        os.chmod(settings_path, 0o600)
        logger.info(f"Node-RED settings file written and secured at {settings_path}.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error installing or configuring Node-RED: {e}")
        raise

if __name__ == "__main__":
    logger.info("Testing Mosquitto installation and configuration.")
    install_mosquitto(mode="private")

    logger.info("Testing Node-RED installation and configuration.")
    install_node_red()
