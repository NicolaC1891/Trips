"""
All handlers for the Belarusian trips branch.

This module registers all the callback query handlers for all messages in the process of Belarusian trips.
Each handler corresponds to a specific step of the process.

The router to process all relevant handlers is created here.
"""

from aiogram import F, Router
from aiogram.types import CallbackQuery

import trips_home.keyboards_home as kb_home
from common.utils import fetch_db_message
from database.models import MessageMenu


def register_handler(filter_value: str, keyboard):
    """
    Registers a callback query handler for a specific filter value and keyboard markup.
    Generates a handler for a given callback data (`filter_value`) and sends a corresponding
    response message with a specific keyboard (`keyboard`) in the callback query.

    Args:
    - filter_value: The callback data that will trigger the handler.
                         Used for the query filter and as the key for fetching the message from DB.
    - keyboard: The inline keyboard markup that will be sent with the response message.
    Returns:
    - None. The factory creates and registers the handler.
    """

    @router_trips_home.callback_query(F.data == filter_value)
    async def create_home_handler(callback_query: CallbackQuery):
        await callback_query.answer()
        message_text = await fetch_db_message(key=filter_value, table=MessageMenu)
        await callback_query.message.answer(text=message_text, reply_markup=keyboard)



def register_trips_home_handlers():
    """
    Registers all the handlers for the Belarusian trips branch.

    This function calls the `register_handler` function for each feature in the Belarusian trips flow,
    passing the appropriate callback data and keyboard for each feature.

    Returns:
    - None. Registers all handlers.
    """
    register_handler(filter_value="home_module", keyboard=kb_home.home_module_kb)
    register_handler(filter_value="home_memo", keyboard=kb_home.home_memo_kb)
    register_handler(filter_value="home_memo_fill", keyboard=kb_home.home_memo_fill_kb)
    register_handler(
        filter_value="home_memo_upload", keyboard=kb_home.home_memo_upload_kb
    )
    register_handler(
        filter_value="home_memo_final", keyboard=kb_home.home_memo_finalize_kb
    )
    register_handler(
        filter_value="home_memo_approve", keyboard=kb_home.home_memo_approve_kb
    )
    register_handler(filter_value="home_order", keyboard=kb_home.home_order_kb)
    register_handler(filter_value="home_trip", keyboard=kb_home.home_trip_kb)
    register_handler(filter_value="home_report", keyboard=kb_home.home_report_kb)
    register_handler(
        filter_value="home_report_pdf", keyboard=kb_home.home_report_pdf_kb
    )
    register_handler(
        filter_value="home_report_paper", keyboard=kb_home.home_report_paper_kb
    )


router_trips_home = Router()
register_trips_home_handlers()
