from apscheduler.schedulers.asyncio import AsyncIOScheduler

from features.advance_report.jobs import send_report_reminder, delete_outdated_reminders


def create_scheduler(my_bot):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_report_reminder, "cron", hour=13, args=[my_bot])
    scheduler.add_job(delete_outdated_reminders, "cron", hour=23)
    return scheduler
