import logging

from logger.log import create_logger


def test_logger_instance():
    logger = create_logger()
    assert isinstance(logger, logging.Logger)


def test_logger_does_not_duplicate_handlers():
    logger1 = create_logger()
    handlers1 = len(logger1.handlers)
    logger2 = create_logger()
    handlers2 = len(logger2.handlers)
    assert handlers1 == handlers2
