from apscheduler.schedulers.asyncio import AsyncIOScheduler

from infrastructure.scheduler.adv_report_jobs import send_report_reminder, delete_outdated_reminders


def create_scheduler(my_bot):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_report_reminder, "cron", hour=12, args=[my_bot])
    scheduler.add_job(delete_outdated_reminders, "cron", hour=23)
    return scheduler