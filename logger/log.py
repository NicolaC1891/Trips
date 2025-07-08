"""
Logging configuration for the bot.

Defines and exports a reusable logger instance,
which writes messages to standard output.
"""

import logging
import sys


def create_logger():
    """
    Creates and configures a logger instance for the application.

    :return: logging.Logger: configured logger with StreamHandler and formatted output
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        handler = logging.StreamHandler(stream=sys.stdout)
        handler.setFormatter(
            logging.Formatter(fmt="[%(asctime)s: %(levelname)s] %(message)s")
        )
        logger.addHandler(handler)
    return logger


logger = create_logger()
