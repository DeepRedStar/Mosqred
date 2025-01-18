import logging

def setup_logger(name, log_file, level=logging.INFO):
    """
    Configure and return a logger.
    Args:
        name (str): Name of the logger.
        log_file (str): Path to the log file.
        level: Logging level (default: logging.INFO).
    Returns:
        logging.Logger: Configured logger instance.
    """
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger
