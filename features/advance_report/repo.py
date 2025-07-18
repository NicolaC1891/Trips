from datetime import date

from sqlalchemy import select

from infrastructure.database.ORMmodels import ReportReminder


class ReminderRepo:
    def __init__(self, session):
        self.session = session

    async def create_record(self, reminder):
        self.session.add(reminder)
        await self.session.commit()

    async def record_exists(
        self,
        user_id: int,
        return_date: date,
        reminder_date: date,
        report_deadline: date,
    ) -> bool:
        statement = select(ReportReminder).where(
            ReportReminder.user_id == user_id,
            ReportReminder.return_date == return_date,
            ReportReminder.reminder_date == reminder_date,
            ReportReminder.report_deadline == report_deadline,
        )

        result = await self.session.execute(statement)
        return result.scalar_one_or_none() is not None
