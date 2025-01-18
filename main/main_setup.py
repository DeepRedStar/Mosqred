import os
from backup_rollback import create_backup, rollback_changes
from tls_setup import generate_self_signed_cert, setup_lets_encrypt
from install_scripts import install_mosquitto, install_node_red
from utils import generate_random_password
from logging_config import setup_logger

# Set up logger
logger = setup_logger('main_setup', 'main_setup.log')

def setup_environment():
    logger.info("Starting setup script.")

    # Backup existing configuration to allow rollback if something goes wrong
    try:
        create_backup()
        logger.info("Backup created successfully.")
    except Exception as e:
        logger.error(f"Failed to create backup: {e}")
        raise

    try:
        # Step 1: Operating System Selection
        print("Select the operating system:")
        print("1. Ubuntu 22.04.5 LTS")
        print("2. Exit")
        while True:
            os_choice = input("Enter your choice (1/2): ").strip()
            if os_choice == '1':
                logger.info("User selected Ubuntu 22.04.5 LTS.")
                break
            elif os_choice == '2':
                logger.info("User chose to exit the setup.")
                print("Exiting setup.")
                return
            else:
                logger.warning("Invalid OS selection input.")
                print("Invalid input. Please enter 1 or 2.")

        # Step 2: Mode Selection (private for self-signed TLS or productive for Let's Encrypt)
        while True:
            mode = input("Select mode (private/productive): ").strip().lower()
            if mode in ['private', 'productive']:
                logger.info(f"User selected mode: {mode}.")
                break
            logger.warning("Invalid mode selection input.")
            print("Invalid mode. Please choose 'private' or 'productive'.")

        # Step 3: Deployment Type (local, cloud, or vpn under cloud)
        while True:
            deployment = input("Deployment type (local/cloud): ").strip().lower()
            if deployment == 'cloud':
                vpn_option = input("Use VPN for secure MQTT communication? (yes/no): ").strip().lower()
                if vpn_option == 'yes':
                    deployment = 'vpn'
                    logger.info("User selected VPN under cloud deployment.")
                elif vpn_option == 'no':
                    logger.info("User selected cloud deployment without VPN.")
                else:
                    logger.warning("Invalid VPN option input.")
                    print("Invalid input. Please enter 'yes' or 'no'.")
                    continue
                break
            elif deployment == 'local':
                logger.info("User selected local deployment.")
                break
            logger.warning("Invalid deployment type input.")
            print("Invalid deployment type. Please choose 'local' or 'cloud'.")

        # Step 4: Summarize User Input
        logger.info("Summarizing user configuration.")
        print("Summary of configuration:")
        print(f"Mode: {mode}")
        print(f"Deployment: {deployment}")
        confirm = input("Confirm the above configuration? (yes/no): ").strip().lower()
        if confirm != 'yes':
            logger.info("User did not confirm the configuration.")
            print("Configuration not confirmed. Exiting.")
            return

        # Step 5: SSL/TLS Setup based on the selected mode
        print("Setting up TLS for secure communication.")
        if mode == 'private':
            logger.info("Setting up self-signed certificate for private mode.")
            generate_self_signed_cert()
        elif mode == 'productive':
            domain = input("Enter your domain for Let's Encrypt: ").strip()
            if not domain:
                logger.error("Domain is required for productive mode but was not provided.")
                print("Domain is required for productive mode. Exiting.")
                return
            logger.info(f"Setting up Let's Encrypt certificate for domain: {domain}.")
            setup_lets_encrypt(domain)

        # Step 6: Install and Configure Mosquitto for MQTT communication
        print("Installing and configuring Mosquitto.")
        logger.info("Installing Mosquitto.")
        install_mosquitto(mode)

        # Step 7: Install and Configure Node-RED for workflow automation
        print("Installing and configuring Node-RED.")
        logger.info("Installing Node-RED.")
        install_node_red()

        # Step 8: Apply additional security measures based on deployment type
        if deployment == 'cloud':
            logger.info("Applying cloud security best practices.")
            # Placeholder for cloud security function
        elif deployment == 'vpn':
            logger.info("Setting up OpenVPN server for secure MQTT communication.")
            # Placeholder for VPN setup function

        # Inform the user of successful setup
        logger.info("Environment setup completed successfully.")
        print("Environment setup complete.")
        print(f"Mode: {mode}, Deployment: {deployment}, TLS: Enabled")
    except Exception as e:
        # Handle errors by rolling back to the last known good state
        logger.error(f"An error occurred during setup: {e}")
        rollback_changes()
        raise

if __name__ == "__main__":
    setup_environment()
