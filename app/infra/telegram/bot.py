from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.config.settings import config
from app.infra.telegram.metadata import COMMANDS, LABEL, DESCRIPTION


def create_bot():
    bot = Bot(
        token=config.TELEGRAM.BOT_TOKEN.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    return bot


async def set_metadata(bot):
    await bot.set_my_commands(COMMANDS)
    await bot.set_my_description(LABEL)
    await bot.set_my_short_description(DESCRIPTION)

