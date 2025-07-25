from datetime import date

from app.infra.logs.logger import logger
from app.application.usecases.advance_report.exceptions import DuplicateReminderError
from workalendar.europe import Belarus
import calendar

from app.application.interfaces.adv_rep_reminder_i import ReminderRepoInterface
from app.application.interfaces.business_flow_i import FlowRepoInterface
from app.infra.rel_db.SQLA import ReportReminder


class AskTripArrivalDateUseCase:

    def __init__(self, repo: FlowRepoInterface, prefix: str, year_str: str, month_str: str):
        self.repo = repo
        self.prefix = prefix
        self.year = int(year_str)
        self.month = int(month_str)

    async def execute(self):

        match self.prefix:

            case "today":
                self.year = date.today().year
                self.month = date.today().month

            case "prev":
                self.month -= 1
                if self.month == 0:
                    self.month = 12
                    self.year -= 1

            case "next":
                self.month += 1
                if self.month == 13:
                    self.month = 1
                    self.year += 1

            case _:
                logger.error("ShowCalendar error: unknown prefix")
                raise ValueError("Unknown month prefix")

        days = calendar.Calendar().monthdayscalendar(self.year, self.month)
        response = await self.repo.get_response("advance_ask_data")

        return response, self.year, self.month, days


class GetAdvanceReportDeadlineUseCase:

    def __init__(self, year_str: str, month_str: str, day_str: str):
        self.year = int(year_str)
        self.month = int(month_str)
        self.day = int(day_str)

    async def execute(self):
        cal = Belarus()
        return_date = date(self.year, self.month, self.day)
        reminder_date = cal.add_working_days(return_date, 10)
        report_deadline = cal.add_working_days(return_date, 15)
        message = (
            f"Дата возвращения: <b>{return_date.strftime('%d.%m.%Y')}</b>\n"
            f"Дата сдачи отчета: <b>{report_deadline.strftime('%d.%m.%Y')}</b>\n\n"
            f"Я начну напоминать за 5 дней до крайнего срока сдачи отчета. Вы хотите <b>создать напоминание</b>?"
        )

        return return_date, reminder_date, report_deadline, message


class CreateAdvanceReminder:

    def __init__(
            self, repo: ReminderRepoInterface,
            user_id: int,
            return_date: date,
            reminder_date: date,
            report_deadline: date
    ):
        self.repo = repo
        self.user_id = user_id
        self.return_date = return_date
        self.reminder_date = reminder_date
        self.report_deadline = report_deadline

    async def execute(self) -> str:
        if await self.repo.record_exists(
            self.user_id, self.return_date, self.reminder_date, self.report_deadline
        ):
            raise DuplicateReminderError("Reminder already exists")

        reminder = ReportReminder(
            user_id=self.user_id,
            return_date=self.return_date,
            reminder_date=self.reminder_date,
            report_deadline=self.report_deadline,
        )
        await self.repo.create_record(reminder)

        cal = Belarus()
        days_left = cal.get_working_days_delta(date.today(), self.report_deadline)
        message = (f"<b>Напоминание создано!</b>\n\n"
                   f"Дата возвращения: <b>{self.return_date.strftime('%d.%m.%Y')}</b>\n"
                   f"Рабочих дней до сдачи отчета: <b>{days_left}</b>"
                   )

        return message


class ReportReminderUseCase:

    def __init__(self, repo_reminder, repo_message):
        self.repo_reminder = repo_reminder
        self.repo_message = repo_message

    async def execute(self):
        user_data = await self.repo_reminder.get_today_reminders()
        response = await self.repo_message.get_response("advance_notify")
        return user_data, response


class DeleteReminderUseCase:

    def __init__(self, repo, user_id, return_date):
        self.repo = repo
        self.user_id = user_id
        self.return_date = return_date

    async def execute(self):

        await self.repo.delete_record(self.user_id, self.return_date)

