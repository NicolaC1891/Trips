import asyncio
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from infrastructure.monitoring.sentry import init_sentry
from infrastructure.scheduler.scheduler_hub import create_scheduler
from infrastructure.telegram.bot_metadata import COMMANDS, LABEL, DESCRIPTION
from infrastructure.telegram.dp_router_hub import create_dispatcher
from settings import config


async def main():

    async with Bot(
        token=config.BOT_TOKEN.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    ) as bot:

        await bot.set_my_commands(COMMANDS)
        await bot.set_my_description(LABEL)
        await bot.set_my_short_description(DESCRIPTION)

        dp = create_dispatcher()

        scheduler = create_scheduler(bot)
        scheduler.start()

        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)


if __name__ == "__main__":
    init_sentry()
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("App terminated")
    except Exception as e:
        print("Unknown error:", type(e).__name__, "-", e)
