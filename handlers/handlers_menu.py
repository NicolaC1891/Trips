"""
All handlers for main menu
"""

from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from keyboards.keyboards_bel import bel_menu_kb
from keyboards.keyboards_menu import main_menu_kb, back_to_main_kb
from aiogram.types import CallbackQuery, Message

from keyboards.keyboards_rus import rus_menu_kb
from logger.log import logger
from database.models import MessageMenu
from database.db import async_session_factory


router_menu = Router()


@router_menu.message(CommandStart())
async def cmd_start(message: Message):
    """
    Handler for /start command
    :param message: Message
    :return: Handler registered with router.
    """
    user_name = message.from_user.full_name
    await message.answer(f"<b>Здравствуйте, {user_name}!</b>\n\n"
                         f"Я помогу вам c организацией командировки: подскажу, как оформить документы, "
                         f"согласовать поездку и что делать по возвращении.\n\n"
                         f"<b>Какая командировка вас интересует?</b>", reply_markup=main_menu_kb)

@router_menu.message(Command('help'))
async def cmd_help(message: Message):
    """
    Handler for /help command
    :param message: Message
    :return: Handler registered with router.
    """
    async with async_session_factory() as session:
        query = select(MessageMenu).filter_by(key='help')
        try:
            statement = await session.scalar(query)
            if not statement:
                await message.answer('Извините, запрашиваемая информация временно недоступна.')
                logger.error(f'Запись с ключом help не найдена')
                return
        except SQLAlchemyError as e:
            logger.error(f"Ошибка выполнения запроса: {e}")
            await message.answer('Произошел сбой. Пожалуйста, попробуйте позже')
            return
        await message.answer(statement.answer, reply_markup=back_to_main_kb)



def register_handler(filter_value: str, keyboard):
    """
    Factory of main menu handlers
    :param filter_value: str
    :param keyboard: Keyboard for message markup
    :return: Handler registered with router
    """
    @router_menu.callback_query(F.data == filter_value)
    async def create_handler(callback_query: CallbackQuery):
        async with async_session_factory() as session:
            query = select(MessageMenu).filter_by(key=filter_value)
            try:
                statement = await session.scalar(query)
                if not statement:
                    await callback_query.message.answer('Извините, запрашиваемая информация временно недоступна.')
                    logger.error(f'Запись с ключом {filter_value} не найдена')
                    return
            except SQLAlchemyError as e:
                logger.error(f"Ошибка выполнения запроса: {e}")
                await callback_query.message.answer('Произошел сбой. Пожалуйста, попробуйте позже')
                return
            await callback_query.answer()
            await callback_query.message.answer(statement.answer, reply_markup=keyboard)


register_handler(filter_value='travel_bel', keyboard=bel_menu_kb)
register_handler(filter_value='travel_rus', keyboard=rus_menu_kb)
register_handler(filter_value='faq', keyboard=back_to_main_kb)
register_handler(filter_value='help', keyboard=back_to_main_kb)
register_handler(filter_value='feedback', keyboard=back_to_main_kb)
register_handler(filter_value='to_main', keyboard=main_menu_kb)
