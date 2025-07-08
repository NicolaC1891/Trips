from datetime import date, timedelta

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup)

from advance_report.logic_adv import (adv_write_cache_to_db,
                                      calculate_reporting_date)
from common.utils import fetch_db_message, format_date
from database.models import MessageMenu
from FSM_Cache.fsm_cache_model import FSMCache
from logger.log import logger
from main_menu.keyboards_menu import main_menu_kb

router_adv = Router()


@router_adv.callback_query(F.data.startswith("day_"))
async def handle_rep_day_selection(query: CallbackQuery, state: FSMContext):
    """
    Handles the user's date selection from the calendar.

    Parses the selected date from the callback data, calculates the reporting
    and reminder dates, saves them to FSM cache, and presents an option
    to create a notification, change the date, or exit the menu.

    Args:
    - query (CallbackQuery): The callback query containing the selected date.
    - state (FSMContext): The FSM context for the user session.
    """

    year, month, day = [int(num) for num in query.data.removeprefix("day_").split("_")]
    selected_date = date(year, month, day)
    reporting_date, notification_date = calculate_reporting_date(selected_date)
    cache = FSMCache(state)
    await cache.update_data(
        "calendar",
        selected_date=selected_date,
        reporting_date=reporting_date,
        notification_date=notification_date,
    )  # Cache all three dates
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Создать напоминание", callback_data="adv_create_reminder"
                )
            ],
            [InlineKeyboardButton(text="✏️ Изменить дату", callback_data="my_calendar")],
            [
                InlineKeyboardButton(
                    text="❌ Отказаться и выйти", callback_data="exit_adv_report"
                )
            ],
        ]
    )

    await query.message.edit_text(
        text=f"🚂 Дата возвращения: {format_date(selected_date)}\n"
        f"⏰ Дата сдачи отчета: <b>{format_date(reporting_date - timedelta(days=1))}</b>\n\n"
        f"Напомнить вам за день до срока сдачи отчета?",
        reply_markup=markup,
    )
    await query.answer()


@router_adv.callback_query(F.data == "exit_adv_report")
async def handle_exit_adv_report(query: CallbackQuery, state: FSMContext):
    """
    Clears calendar-related cache and sends the main menu message.

    Args:
    - query (CallbackQuery): The callback query containing the selected date.
    - state (FSMContext): The FSM context for the user session.
    """
    cache = FSMCache(state)
    await cache.clear_data("calendar")
    message_text = await fetch_db_message(key="to_main", table=MessageMenu)
    await query.message.answer(text=message_text, reply_markup=main_menu_kb)
    await query.answer()


@router_adv.callback_query(F.data == "adv_create_reminder")
async def handle_create_reminder(query: CallbackQuery, state: FSMContext):
    """
    Handles creation of a reminder based on the selected calendar date.
    Saves the reminder in DB and returns the user to the main menu.

    Args:
    - query (CallbackQuery): The callback query containing the selected date.
    - state (FSMContext): The FSM context for the user session.
    """
    cache = FSMCache(state)
    try:
        all_data = await cache.get_data("calendar")
        user_id: int = query.from_user.id
        report_deadline: date | None = all_data.get("reporting_date")
        reminder_date: date | None = all_data.get("notification_date")
        return_date: date | None = all_data.get("selected_date")
        if not all([report_deadline, reminder_date, return_date]):
            await query.answer("Произошла ошибка. Выберите дату еще раз.")
            logger.error("Error: no date found.")
            return
    except Exception as e:
        await query.answer("Произошла ошибка")
        logger.error(f"Error reading from cache: {str(e)}")
        return

    if report_deadline < date.today():
        await query.answer(
            text="❌ Срок сдачи авансового отчета уже прошёл!", show_alert=True
        )
    elif reminder_date <= date.today():
        await query.answer(
            text="⏰ Напоминание уже не актуально — пора сдавать отчет!",
            show_alert=True,
        )
    else:
        await adv_write_cache_to_db(
            user_id, return_date, reminder_date, report_deadline
        )
        await query.answer(text="🗓 Напоминание создано!")
    await cache.clear_data("calendar")
    message_text = await fetch_db_message(key="to_main", table=MessageMenu)
    await query.message.answer(text=message_text, reply_markup=main_menu_kb)
    await query.answer()
