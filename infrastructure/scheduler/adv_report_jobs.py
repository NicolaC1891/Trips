from datetime import datetime

from sqlalchemy import delete, func, select

from infrastructure.database.session import async_session_factory
from infrastructure.database.ORMmodels import ReportReminder
from common.logger.logger import logger


async def send_report_reminder(bot):
    """
    Sends reminders to users whose report submission deadline is tomorrow.

    This function queries the database for all `ReportReminder` entries where
    the `reminder_date` matches today's date. For each reminder, it sends a message
    to the associated user via the provided bot.

    Args:
    - bot: An instance of the bot used to send messages.

    Logs:
    - Errors if message sending fails for a user.
    """

    async with async_session_factory() as session:
        today = datetime.today()
        query = select(ReportReminder).where(
            func.date(ReportReminder.reminder_date) == today.date()
        )
        statement = await session.execute(query)
        reminders = statement.scalars().all()
        for reminder in reminders:
            try:
                await bot.send_message(
                    chat_id=reminder.user_id,
                    text="Сегодня последний день сдачи отчета!",
                )
            except Exception as e:
                logger.error(f"Failed to send reminder to user {reminder.user_id}: {e}")


async def delete_outdated_reminders():
    """
    Deletes outdated report reminders from the database.

    This function removes all `ReportReminder` entries from the database where
    the `report_deadline` is earlier than today's date.

    Logs:
    - Number of rows marked for deletion and number of rows successfully deleted.
    """
    async with async_session_factory() as session:
        today = datetime.today()
        query = delete(ReportReminder).where(
            func.date(ReportReminder.report_deadline) < today.date()
        )
        result = await session.execute(query)
        logger.info(f"Rows to be deleted: {result.rowcount}")
        await session.commit()
        logger.info(f"Deleted {result.rowcount} outdated entries")
