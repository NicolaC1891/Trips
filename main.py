import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from advance_report.handlers_adv import router_adv
from logger.log import logger
from main_menu.handlers_menu import router_menu
from my_calendar.handlers_cal import router_calendar
from schedules.adv_report_jobs import (delete_outdated_reminders,
                                       send_report_reminder)
from settings import config
from trips_abroad.handlers_abroad import router_trips_abroad
from trips_home.handlers_home import router_trips_home

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


commands = [
    BotCommand(command="start", description="Начало работы"),
    BotCommand(command="help", description="Помощь"),
]


async def main():
    """
    Initializes and starts the Telegram bot.

    This function:
    - Creates a bot instance with HTML parse mode.
    - Sets bot commands.
    - Configures the dispatcher with startup and shutdown handlers.
    - Registers all necessary routers.
    - Schedules periodic background tasks using `APScheduler`.
    - Drops pending updates and starts polling for new updates.

    Returns:
    - None
    """
    async with Bot(
        token=config.BOT_TOKEN.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    ) as bot:
        await bot.set_my_commands(commands=commands)
        await bot.set_my_description("Командировки v.0.9 beta")
        await bot.set_my_short_description('Помощник для работников "Сбер Банк" (Беларусь) при оформлении командировок')
        dp = Dispatcher()
        dp.startup.register(startup)
        dp.shutdown.register(shutdown)
        dp.include_routers(
            router_menu,
            router_trips_home,
            router_trips_abroad,
            router_calendar,
            router_adv,
        )
        scheduler = AsyncIOScheduler()
        scheduler.add_job(send_report_reminder, "cron", hour=12, args=[bot])
        scheduler.add_job(delete_outdated_reminders, "cron", hour=23)
        scheduler.start()
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)


async def startup():
    logger.info("Bot launched...")


async def shutdown():
    logger.info("Bot terminated...")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("App terminated")
    except Exception as e:
        print("Unknown error:", type(e).__name__, "-", e)
