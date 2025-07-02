import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.exceptions import AiogramError

from settings import config
from aiogram.client.default import DefaultBotProperties
from handlers.handlers_menu import router_menu
from handlers.handlers_bel import router_bel
from logger.log import logger


async def main():
    bot = Bot(token=config.BOT_TOKEN.get_secret_value(), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.startup.register(startup)
    dp.shutdown.register(shutdown)
    dp.include_routers(router_menu, router_bel)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


async def startup():
    logger.info("Bot launched...")


async def shutdown():
    logger.info("Bot terminated...")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except AiogramError:
        print("Unknown error")
    except KeyboardInterrupt:
        print("App terminated")
