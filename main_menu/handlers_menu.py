"""
All handlers for the main menu.

This module defines all command and callback query handlers related to the bot's main menu.

Features:
- Handles the /start and /help commands.
- Handles main menu callback queries (e.g., travel options, instructions, feedback).
- Dynamically generates handlers for static content using a factory function.
- Includes a special handler for the "Cat-bot" and the calendar-based advance report.

Functions:
- cmd_start: Greets the user and displays the main menu.
- cmd_help: Shows help information from the database.
- register_main_handler: Factory function for creating simple menu handlers.
- register_cat_handler: Shows a daily cat wisdom message.
- adv_report_handler: Starts the advance report flow with a calendar.
- register_all_menu_handlers: Registers multiple static content handlers.
"""

from datetime import date

from aiogram import F, Router
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from advance_report.fsm_states import AdvReportStates
from cat_bot.daily_wisdom import get_today_wisdom
from common.utils import fetch_db_message
from database.db import async_session_factory
from database.models import MessageMenu
from FSM_Cache.fsm_cache_model import FSMCache
from main_menu.keyboards_menu import back_to_main_kb, main_menu_kb
from my_calendar.generator_cal import build_calendar
from trips_abroad.keyboards_abroad import abroad_menu_kb
from trips_home.keyboards_home import home_menu_kb

router_menu = Router()

# COMMANDS


@router_menu.message(CommandStart(deep_link=True))
async def cmd_start(message: Message, command: CommandObject, state: FSMContext):
    """
    Handles the /start command.
    Greets the user and displays the main menu with a message fetched from the database.

    Args:
    - message (Message): The incoming Telegram message.
    """
    await state.clear()

    user_name = message.from_user.full_name
    message_text = await fetch_db_message(key="to_main", table=MessageMenu)

    await message.answer(
        f"<b>Здравствуйте, {user_name}!</b>\n\n{message_text}",
        reply_markup=main_menu_kb,
    )


@router_menu.message(Command("help"))
async def cmd_help(message: Message):
    """
    Handles the /help command.
    Sends help/instruction text stored in the database along with a back-to-main keyboard.

    Args:
    - message (Message): The incoming Telegram message.
    """
    message_text = await fetch_db_message(key="help", table=MessageMenu)
    await message.answer(text=message_text, reply_markup=back_to_main_kb)


# MENU HANDLERS


def register_main_handler(filter_value: str, keyboard):
    """
    Registers a callback handler for a static menu section.
    Fetches the associated message from the database and displays it with the specified keyboard.

    Args:
    - filter_value (str): The callback data to listen for.
    - keyboard: The reply markup (keyboard) to attach to the response.
    """

    @router_menu.callback_query(F.data == filter_value)
    async def create_main_handler(callback_query: CallbackQuery):
        message_text = await fetch_db_message(key=filter_value, table=MessageMenu)
        await callback_query.message.answer(message_text, reply_markup=keyboard)


@router_menu.callback_query(F.data == "cat_bot")
async def register_cat_handler(callback_query: CallbackQuery):
    """
    Handles the 'Cat-bot' menu item.
    Sends a message from the database along with a daily cat wisdom phrase.
    """
    base_message = await fetch_db_message(key="cat_bot", table=MessageMenu)
    async with async_session_factory() as session:
        cat_wisdom = await get_today_wisdom(session)
    final_message = f"{base_message}\n\n{cat_wisdom}"
    await callback_query.message.answer(final_message, reply_markup=back_to_main_kb)
    await callback_query.answer()


@router_menu.callback_query(F.data == "my_calendar")
async def adv_report_handler(callback_query: CallbackQuery, state: FSMContext):
    """
    Handles the advance report calendar feature.
    Sets the FSM state for the feature, clears previous cached data,
    and sends an inline calendar to the user.

    Args:
    - callback_query (CallbackQuery): The incoming callback.
    - state (FSMContext): FSM context for managing state transitions within the feature.
    """
    await state.set_state(AdvReportStates.date_selection)  # Feature entry point
    cache = FSMCache(state)
    await cache.clear_data(
        "calendar"
    )  # Because user can go back to date selection after initial selection
    today = date.today()
    year, month = today.year, today.month
    message_text = await fetch_db_message(key="my_calendar", table=MessageMenu)
    await callback_query.answer()
    await callback_query.message.answer(
        text=message_text, reply_markup=build_calendar(year, month)
    )


def register_all_menu_handlers():
    """
    Registers all static menu handlers for known callback values in the main menu.
    """
    register_main_handler(filter_value="home_travel", keyboard=home_menu_kb)
    register_main_handler(filter_value="abroad_travel", keyboard=abroad_menu_kb)
    register_main_handler(filter_value="manual", keyboard=back_to_main_kb)
    register_main_handler(filter_value="help", keyboard=back_to_main_kb)
    register_main_handler(filter_value="to_main", keyboard=main_menu_kb)


register_all_menu_handlers()
