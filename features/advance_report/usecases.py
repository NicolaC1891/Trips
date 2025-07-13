from datetime import date
from common.logger.logger import logger
from features.advance_report.exceptions import DuplicateReminderError
from workalendar.europe import Belarus
import calendar

from infrastructure.database.ORMmodels import ReportReminder


class AskTripArrivalDateUseCase:

    def __init__(self, repo, prefix, year_str, month_str):
        self.repo = repo
        self.prefix = prefix
        self.year = int(year_str)
        self.month = int(month_str)

    async def execute(self):

        match self.prefix:

            case 'today':
                self.year = date.today().year
                self.month = date.today().month

            case 'prev':
                self.month -= 1
                if self.month == 0:
                    self.month = 12
                    self.year -= 1

            case 'next':
                self.month += 1
                if self.month == 13:
                    self.month = 1
                    self.year += 1

            case _:
                logger.error('ShowCalendar error: unknown prefix')
                raise ValueError('Unknown month prefix')

        days = calendar.Calendar().monthdayscalendar(self.year, self.month)
        response = await self.repo.get_response('advance_ask_data')

        return response, self.year, self.month, days


class GetAdvanceReportDeadlineUseCase:

    def __init__(self, year_str, month_str, day_str):
        self.year = int(year_str)
        self.month = int(month_str)
        self.day = int(day_str)

    async def execute(self):
        cal = Belarus()
        return_date = date(self.year, self.month, self.day)
        reminder_date = cal.add_working_days(return_date, 14)
        report_deadline = cal.add_working_days(return_date, 15)
        message = (f"Дата возвращения: <b>{return_date}</b>\n"
                   f"Дата сдачи отчета: <b>{report_deadline}</b>\n\n"
                   f"Создать напоминание за день до срока сдачи отчета?")

        return return_date, reminder_date, report_deadline, message


class CreateAdvanceReminder:

    def __init__(self, repo, user_id, return_date, reminder_date, report_deadline):
        self.repo = repo
        self.user_id = user_id
        self.return_date = return_date
        self.reminder_date = reminder_date
        self.report_deadline = report_deadline

    async def execute(self):
        if await self.repo.record_exists(self.user_id, self.return_date, self.reminder_date, self.report_deadline):
            raise DuplicateReminderError("Reminder already exists")
        reminder = ReportReminder(
            user_id=self.user_id,
            return_date=self.return_date,
            reminder_date=self.reminder_date,
            report_deadline=self.report_deadline,
        )
        await self.repo.create_record(reminder)
