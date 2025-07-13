from abc import ABC, abstractmethod


class ReminderRepoInterface(ABC):
    def __init__(self, session):
        self.session = session

    @abstractmethod
    async def create_record(self, reminder):
        pass

    @abstractmethod
    async def record_exists(self, user_id, return_date, reminder_date, report_deadline) -> bool:
        pass
