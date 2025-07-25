from datetime import datetime

from sqlalchemy import delete, func

from app.infra.repositories.adv_rep_reminder_r import ReminderRepo
from app.ui.keyboards.advance_report.adv_rep_kb_builder import AdvanceReminderMessageUI
from app.application.usecases.advance_report.usecases import ReportReminderUseCase
from app.infra.repositories.business_flow_r import FlowRepo
from app.infra.rel_db.session_factory import async_session_factory
from app.infra.rel_db.SQLA import ReportReminder
from app.infra.logs.logger import logger


async def send_report_reminder(notifier):
    async with async_session_factory() as session:
        repo_reminder = ReminderRepo(session)
        repo_message = FlowRepo(session)
        use_case = ReportReminderUseCase(repo_reminder, repo_message)
        user_data, message = await use_case.execute()

        for user_item in user_data:
            try:
                full_message = message.format(user_item.return_date.strftime('%d.%m.%Y'), user_item.report_deadline.strftime('%d.%m.%Y'))
                return_date = user_item.return_date
                callback_key = f"{return_date.year}_{return_date.month}_{return_date.day}"
                keyboard = AdvanceReminderMessageUI(callback_key).build_kb()
                await notifier.send_message(
                    chat_id=user_item.user_id,
                    text=full_message, reply_markup=keyboard
                )
            except Exception as e:
                logger.error(f"Failed to send reminder to user {user_item.user_id}: {e}")


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
