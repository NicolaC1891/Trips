
class ReportDeadlinePassedError(Exception):
    """
    Exception to be raised when the report deadline is already in the past.
    """
    pass


class ReminderTooLateError(Exception):
    """
    Exception to be raised when the reminder date is today or on a certain date in the past.
    """
    pass