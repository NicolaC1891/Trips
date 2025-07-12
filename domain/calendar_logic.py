import calendar


class CalendarCalculator:
    @staticmethod
    def get_calendar_by_month(year, month):
        calendar_days = calendar.Calendar().monthdayscalendar(year=year, month=month)
        return calendar_days
