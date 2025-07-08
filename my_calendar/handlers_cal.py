from datetime import date

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery

from my_calendar.generator_cal import build_calendar

router_calendar = Router()


@router_calendar.callback_query(F.data.startswith("prev_"))
async def handle_prev_month(query: CallbackQuery):
    """
    Handles callback query to navigate to the previous month in the calendar.

    Extracts the current year and month from the callback data, calculates the previous month,
    rebuilds the calendar markup, and updates the inline keyboard.

    Args:
    - query (CallbackQuery): The callback query containing data like 'prev_2025_07'.
    """
    await query.answer()
    year, month = [int(num) for num in query.data.removeprefix("prev_").split("_")]
    month -= 1
    if month == 0:
        month = 12
        year -= 1
    markup = build_calendar(year, month)
    await query.message.edit_reply_markup(reply_markup=markup)



@router_calendar.callback_query(F.data.startswith("next_"))
async def handle_next_month(query: CallbackQuery):
    """
    Handles callback query to navigate to the next month in the calendar.

    Extracts the current year and month from the callback data, calculates the next month,
    rebuilds the calendar markup, and updates the inline keyboard.

    Args:
    - query (CallbackQuery): The callback query containing data like 'next_2025_07'.
    """
    await query.answer()
    year, month = [int(num) for num in query.data.removeprefix("next_").split("_")]
    month += 1
    if month == 13:
        month = 1
        year += 1
    markup = build_calendar(year, month)
    await query.message.edit_reply_markup(reply_markup=markup)



@router_calendar.callback_query(F.data == "reset_calendar")
async def handle_reset_calendar(query: CallbackQuery):
    """
    Handles callback query to reset the calendar to the current month.

    Rebuilds the calendar for today's date and updates the inline keyboard.
    If the message is already displaying the current month, it evades Telegram behavior
    when markup may fail to attach if the contents of the message and the markup remain the same.

    Args:
    - query (CallbackQuery): The callback query with data 'reset_calendar'.
    """
    await query.answer()
    today = date.today()
    markup = build_calendar(today.year, today.month)
    try:
        await query.message.edit_reply_markup(reply_markup=markup)
    except TelegramBadRequest as e:
        if "message is not modified" in str(
            e
        ):  # Circumventing Telegram specific behavior with same content answers
            pass
        else:
            raise



@router_calendar.callback_query(F.data == "ignore")
async def handle_reset_calendar(query: CallbackQuery):
    """
    Handles clicks on inactive calendar buttons (headers, empty cells, etc.).
    Simply removes the button highlight without performing any action.
    """
    await query.answer()
    pass
