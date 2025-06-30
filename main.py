import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from settings import config
from aiogram.client.default import DefaultBotProperties
from handlers import router_menu


async def main():
    bot = Bot(token=config.bot_token.get_secret_value(), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.startup.register(startup)
    dp.shutdown.register(shutdown)
    dp.include_router(router_menu)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


async def startup():
    logger.info("Bot launched...")


async def shutdown():
    logger.info("Bot terminated...")


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("App terminated")
