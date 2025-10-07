from datetime import date
import calendar


def get_calendar_days(year, month):
    days = calendar.Calendar().monthdayscalendar(year, month)
    return days


def navigate_calendar(action, year, month):

    match action:

        case "caltoday":
            year = date.today().year
            month = date.today().month

        case "calprev":
            month -= 1
            if month == 0:
                month = 12
                year -= 1

        case "calnext":
            month += 1
            if month == 13:
                month = 1
                year += 1

    days = get_calendar_days(year, month)
    return year, month, days
