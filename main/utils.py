import secrets
import string
from logging_config import setup_logger

# Set up logger
logger = setup_logger('utils', 'utils.log')

def generate_random_password(length=64):
    """Generate a secure random password."""
    if not isinstance(length, int) or length <= 0:
        logger.error("Invalid password length provided. Must be a positive integer.")
        raise ValueError("Length must be a positive integer.")

    characters = string.ascii_letters + string.digits + string.punctuation
    logger.info(f"Generating a random password of length {length}.")
    password = ''.join(secrets.choice(characters) for _ in range(length))
    logger.info("Password generation successful.")
    return password

if __name__ == "__main__":
    try:
        print("Generated Password (default):", generate_random_password())
        print("Generated Password (16 chars):", generate_random_password(16))
    except ValueError as e:
        logger.error(f"Error during password generation: {e}")
        print("Error:", e)
