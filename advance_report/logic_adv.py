from datetime import timedelta

import holidays

from database.db import async_session_factory
from database.models import ReportReminder
from logger.log import logger


def calculate_reporting_date(selected_date):
    """
    Calculates the reporting date and the notification date based on a selected date.

    The function iterates through the dates starting from the selected date and counts
    the working days, excluding weekends and holidays, until it reaches 15 working days.
    The reporting date is the 15th working day, and the notification date is the 14th working day.

    Args:
    - selected_date (date): The date selected by the user as a starting point.

    Returns:
    - tuple: A tuple containing two dates:
      reporting_date (date): The calculated reporting date (15th working day).
      notification_date (date): The calculated notification date (14th working day).
    """
    by_holidays = holidays.country_holidays("BY")
    workday_count = 0
    current_date = selected_date
    notification_date = None
    while workday_count < 15:
        current_date += timedelta(days=1)
        if current_date not in by_holidays and current_date.isoweekday() < 6:
            workday_count += 1
            if workday_count == 14:
                notification_date = current_date
    reporting_date = current_date
    return reporting_date, notification_date


async def adv_write_cache_to_db(user_id, return_date, reminder_date, report_deadline):
    """
    Writes the return from trip, report reminder, and report deadline dates to the database.

    This function creates a new ReportReminder object and stores it in the database
    for the given user, saving their return date, reminder date, and report deadline.

    Args:
    - user_id (int): The ID of the user to associate with the reminder.
    - return_date (date): The date when the user is supposed to return from the business trip.
    - reminder_date (date): The date when a reminder should be sent to the user.
    - report_deadline (date): The final deadline for submitting the report.

    Returns:
    - None: This function does not return any value. It commits the changes directly to the database.
    """
    async with async_session_factory() as session:
        try:
            reminders = ReportReminder(
                user_id=user_id,
                return_date=return_date,
                reminder_date=reminder_date,
                report_deadline=report_deadline,
            )
            session.add(reminders)
            await session.commit()
        except Exception as e:
            logger.error(f"Error writing to database: {e}")
