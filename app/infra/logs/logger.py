"""
Logger with log level dependency on dev/prod
"""
from sqlite3 import IntegrityError
from datetime import date

from app.config.settings import config
import logging
import sys

from app.infra.rel_db.SQLA import UserStats


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


async def log_user(user_id, feature_name, session):
    cur_date = date.today()
    record = UserStats(user_id=user_id, feature_name=feature_name, log_date=cur_date)
    session.add(record)
