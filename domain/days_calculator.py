from datetime import timedelta, date
from typing import Tuple


class DaysCalculator:
    def __init__(self, holidays=None):
        self.holidays = set() if holidays is None else holidays

    @staticmethod
    def add_calendar_days(start, count: int) -> date:
        return start + timedelta(days=count)

    def add_business_days(self, start: date, count: int) -> date:
        current_date = start
        added = 0

        while added < count:
            current_date += timedelta(days=1)
            if current_date not in self.holidays and current_date.isoweekday() < 6:
                added += 1
        end_date = current_date
        return end_date

    def add_business_days_with_checkpoint(self, start: date, count: int, checkpoint: int) -> Tuple[date, date]:
        current_date = start
        added = 0
        checkpoint_date = None
        while added < count:
            current_date += timedelta(days=1)
            if current_date not in self.holidays and current_date.isoweekday() < 6:
                added += 1
                if added == checkpoint:
                    checkpoint_date = current_date
        end_date = current_date
        return checkpoint_date, end_date

    def count_days_between(self, start: date, end: date) -> int:
        pass


