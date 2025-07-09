"""
Office Cat daily wisdom generator.

This module provides functions to select a random phrase (or "wisdom")
from the CatPhrase table. The selection is deterministic per day,
meaning the same phrase will be returned throughout a given day to all users.
"""

import random
from datetime import date

from sqlalchemy import select

from database.models import CatPhrase
from logger.log import logger


def get_daily_random_id(ids: list[int]) -> int:
    """
    Returns a pseudo-random ID from the given list, consistent for the current day.

    The selection is seeded with today's date to ensure that the same ID
    is chosen for every call during a single day, changing daily.

    Args:
    - ids (list[int]): A list of available integer IDs.

    Returns:
    - int: A randomly selected ID that remains consistent for the current day.
    """
    today_seed = date.today().toordinal()
    random.seed(today_seed)
    daily_id = random.choice(ids)
    return daily_id


async def get_today_wisdom(session) -> str:
    """
    Retrieves today's "cat wisdom" phrase from the database.

    Selects all available phrase IDs from the CatPhrase table,
    chooses one based on the current date, and returns the corresponding phrase.
    If no phrases are available, or if the selected one cannot be found,
    returns a fallback message.

    Args:
    - session: An active SQLAlchemy async session.

    Returns:
    - str: The selected wisdom phrase, or a fallback message if unavailable.
    """
    async with session:
        result = await session.execute(select(CatPhrase.id))
        ids = [row[0] for row in result.all()]
        if not ids:
            logger.error("No cat phrases available")
            return "Кот сегодня молчит..."
        random_id = get_daily_random_id(ids)
        try:
            wisdom_query = select(CatPhrase).where(CatPhrase.id == random_id)
        except Exception as e:
            logger.error(f"Error retrieving Cat wisdom: {e}")
        wisdom_res = await session.execute(wisdom_query)
        wisdom = wisdom_res.scalar_one_or_none()
    return wisdom.phrase if wisdom else "Кот потерял мысль..."
