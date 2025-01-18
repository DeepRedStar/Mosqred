import os
import subprocess
from logging_config import setup_logger

# Set up logger
logger = setup_logger('cloud_security', 'cloud_security.log')

def apply_cloud_security():
    """Apply best practices for securing cloud deployments."""
    try:
        logger.info("Starting cloud security configuration.")

        # Ensure UFW is installed
        if not shutil.which("ufw"):
            logger.info("UFW not found. Proceeding with installation.")
            subprocess.run(["sudo", "apt-get", "install", "-y", "ufw"], check=True)
            logger.info("UFW installed successfully.")
        else:
            logger.info("UFW is already installed.")

        # Configure UFW rules
        subprocess.run(["sudo", "ufw", "default", "deny", "incoming"], check=True)
        subprocess.run(["sudo", "ufw", "default", "allow", "outgoing"], check=True)
        subprocess.run(["sudo", "ufw", "allow", "22"], check=True)
        logger.info("SSH (port 22) allowed. Consider limiting access to specific IP addresses for enhanced security.")  # Allow SSH
        subprocess.run(["sudo", "ufw", "allow", "8883"], check=True)  # Allow MQTT over TLS
        logger.info("UFW rules configured.")

        # Enable UFW
        try:
            subprocess.run(["sudo", "ufw", "enable"], check=True)
            logger.info("UFW enabled successfully.")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to enable UFW: {e}")
            raise
        logger.info("UFW enabled successfully.")

        # Install Fail2Ban
        if not shutil.which("fail2ban-client"):
            logger.info("Fail2Ban not found. Proceeding with installation.")
            subprocess.run(["sudo", "apt-get", "install", "-y", "fail2ban"], check=True)
            logger.info("Fail2Ban installed successfully.")
        else:
            logger.info("Fail2Ban is already installed.")

        # Start and enable Fail2Ban service
        if subprocess.run(["sudo", "systemctl", "is-enabled", "fail2ban"], capture_output=True, text=True).returncode == 0:
            logger.info("Fail2Ban is already enabled.")
        else:
            subprocess.run(["sudo", "systemctl", "enable", "fail2ban"], check=True)
            logger.info("Fail2Ban service enabled successfully.")
        subprocess.run(["sudo", "systemctl", "start", "fail2ban"], check=True)
        logger.info("Fail2Ban service started and enabled.")

        logger.info("Cloud security configuration completed successfully.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error during cloud security configuration: {e}")
        raise

if __name__ == "__main__":
    apply_cloud_security()
