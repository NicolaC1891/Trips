import logging
import sys


def create_logger():
    """
    Creates a logger instance.
    :return: logger instance
    """
    logger = logging.getLogger("__name__")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(logging.Formatter(fmt="[%(asctime)s: %(levelname)s] %(message)s"))
    logger.addHandler(handler)
    return logger


logger = create_logger()
