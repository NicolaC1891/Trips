from abc import ABC, abstractmethod
from datetime import date

from infrastructure.database.ORMmodels import ReportReminder


class ReminderRepoInterface(ABC):
    def __init__(self, session):
        self.session = session

    @abstractmethod
    async def create_record(self, reminder: ReportReminder):
        pass

    @abstractmethod
    async def record_exists(
        self, user_id: int, return_date: date, reminder_date: date, report_deadline: date
    ) -> bool:
        pass
