from aiogram import F, Router
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
import keyboards.keyboards_bel as kb_bel
from aiogram.types import CallbackQuery
from logger.log import logger
from database.models import MessageMenu
from database.db import async_session_factory


router_bel = Router()


def register_handler(filter_value, keyboard):
    @router_bel.callback_query(F.data == filter_value)
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


def register_all_handlers():
    register_handler(filter_value='module', keyboard=kb_bel.module_kb)
    register_handler(filter_value='request_all', keyboard=kb_bel.request_all_kb)
    register_handler(filter_value='request', keyboard=kb_bel.form_kb)
    register_handler(filter_value='chancellor', keyboard=kb_bel.output_kb)
    register_handler(filter_value='completion', keyboard=kb_bel.completion_kb)
    register_handler(filter_value='approval', keyboard=kb_bel.approval_kb)
    register_handler(filter_value='order', keyboard=kb_bel.order_kb)
    register_handler(filter_value='on_trip', keyboard=kb_bel.trip_kb)
    register_handler(filter_value='report', keyboard=kb_bel.report_kb)


register_all_handlers()
