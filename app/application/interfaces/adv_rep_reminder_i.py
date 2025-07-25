from abc import ABC, abstractmethod
from datetime import date

from app.infra.rel_db.SQLA import ReportReminder


class ReminderRepoInterface(ABC):

    @abstractmethod
    async def create_record(self, reminder: ReportReminder):
        pass

    @abstractmethod
    async def record_exists(
        self, user_id: int, return_date: date, reminder_date: date, report_deadline: date
    ) -> bool:
        pass

    @abstractmethod
    async def get_today_reminders(self):
        pass

    @abstractmethod
    async def delete_record(self, user_id, return_date):
        pass
