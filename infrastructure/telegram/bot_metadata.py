from aiogram.client import bot
from aiogram.types import BotCommand

COMMANDS = [
    BotCommand(command="start", description="Начало работы"),
    BotCommand(command="help", description="Помощь"),
]

LABEL = "Командировки v.0.9 beta"

DESCRIPTION = 'Помощник для работников "Сбер Банк" (Беларусь) при оформлении командировок'
