import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import BotCommand
from aiogram.client.default import DefaultBotProperties


from settings import config
from handlers.handlers_menu import router_menu
from handlers.handlers_bel import router_bel
from handlers.handlers_rus import router_rus
from logger.log import logger


commands = [BotCommand(command="start", description="Начало работы"), BotCommand(command="help", description="Помощь")]


async def main():
    """
    Launches the bot, connects the dispatcher with startup and shutdown actions, connects routers, starts polling.
    :return:
    """
    async with Bot(
            token=config.BOT_TOKEN.get_secret_value(),
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    ) as bot:
        await bot.set_my_commands(commands=commands)
        dp = Dispatcher()
        dp.startup.register(startup)
        dp.shutdown.register(shutdown)
        dp.include_routers(router_menu, router_bel, router_rus)
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