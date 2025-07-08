from datetime import date

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from database.db import async_session_factory
from logger.log import logger


async def fetch_db_message(key: str, table) -> str:
    async with async_session_factory() as session:
        query = select(table).where(table.key == key)
        try:
            statement = await session.scalar(query)
            if not statement:
                logger.error(f"No entry found with key {key}")
                return "Сообщение не найдено"
        except SQLAlchemyError as e:
            logger.error(f"Error executing database request: {e}")
            return "Ошибка при получении сообщения"
        answer = statement.response
        return answer


def format_date(d: date) -> str:
    return d.strftime("%d.%m.%Y")
