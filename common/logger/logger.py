"""
Logger with log level dependency on dev/prod
"""

from settings import config
import logging
import sys


def create_logger():
    logger = logging.getLogger(__name__)

    # avoid doubling
    if logger.hasHandlers():
        logger.handlers.clear()

    env = config.ENV
    log_level = logging.DEBUG if env == "dev" else logging.INFO
    logger.setLevel(log_level)

    handler = logging.StreamHandler(stream=sys.stdout)
    formatter = logging.Formatter(fmt="[%(asctime)s: %(levelname)s] %(message)s")
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger


logger = create_logger()
