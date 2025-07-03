"""
All handlers for Belarusian trips branch
"""

from aiogram import F, Router
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
import keyboards.keyboards_rus as kb_rus
from aiogram.types import CallbackQuery
from logger.log import logger
from database.models import MessageMenu
from database.db import async_session_factory


router_rus = Router()


def register_handler(filter_value: str, keyboard) -> None:
    """
    Factory of Foreign trips tree handlers
    :param filter_value: String value used for router filter, query filter, and db key
    :param keyboard: Keyboard for answer markup
    :return: None
    """
    @router_rus.callback_query(F.data == filter_value)
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


def register_all_handlers() -> None:
    """
    Registers all handlers within one function.
    :return: None
    """
    register_handler(filter_value='module_r', keyboard=kb_rus.module_r_kb)
    register_handler(filter_value='memo', keyboard=kb_rus.memo_kb)
    register_handler(filter_value='request_r', keyboard=kb_rus.form_r_kb)
    register_handler(filter_value='chancellor_r', keyboard=kb_rus.output_r_kb)
    register_handler(filter_value='completion_r', keyboard=kb_rus.completion_r_kb)
    register_handler(filter_value='approval_r', keyboard=kb_rus.approval_r_kb)
    register_handler(filter_value='order_r', keyboard=kb_rus.order_r_kb)
    register_handler(filter_value='on_trip_r', keyboard=kb_rus.trip_r_kb)
    register_handler(filter_value='report_r', keyboard=kb_rus.report_r_kb)
    register_handler(filter_value='report_r_pdf', keyboard=kb_rus.report_r_pdf_kb)
    register_handler(filter_value='report_r_paper', keyboard=kb_rus.report_r_paper_kb)


register_all_handlers()
