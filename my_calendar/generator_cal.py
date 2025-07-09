"""
This module provides utility functions to generate an interactive inline calendar
keyboard for Telegram bots using Aiogram. It supports navigation between months,
displaying the current day with a special marker, and allows users to select dates.

Features:
- Calendar header with previous/next month navigation
- Weekday labels in Russian (abbreviated)
- Day grid with current day highlight
- Footer with reset and navigation options

Functions:
- generate_calendar_header(year, month): Creates navigation buttons and a title label.
- generate_weekdays_row(): Creates a row of weekday name buttons.
- generate_month_days(year, month): Creates a grid of days for the month.
- generate_calendar_footer(): Creates a footer row with reset and back buttons.
- build_calendar(year, month): Assembles all components into a full inline calendar.

Dependencies:
- Aiogram's `InlineKeyboardMarkup` and `InlineKeyboardButton`
- The `calendar` and `datetime` standard libraries
- `MONTHS_RU` and `DAYS_RU` constants for Russian month/day names
- `back_to_main_button()` for returning to the main menu (assumed to be defined elsewhere)

Intended to be used with callback query handlers that respond to calendar navigation.

Example usage:
markup = build_calendar(2025, 7)
await bot.send_message(chat_id, "Select a date:", reply_markup=markup)
"""

import calendar
from datetime import date

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from common.buttons import back_to_main_button
from my_calendar.models_cal import DAYS_RU, MONTHS_RU


def generate_calendar_header(year: int, month: int) -> list[InlineKeyboardButton]:
    """
    Generates the header row of the inline calendar.

    Includes navigation buttons to move to the previous and next months,
    and a label displaying the current month and year.

    Args:
    - year (int): The current year.
    - month (int): The current month (1–12).

    Returns:
    - list[InlineKeyboardButton]: A list of three buttons for the header row.
    """
    buttons = [
        InlineKeyboardButton(text="⏪", callback_data=f"prev_{year}_{month}"),
        InlineKeyboardButton(
            text=f"{MONTHS_RU[month - 1].name} {year}", callback_data="ignore"
        ),
        InlineKeyboardButton(text="⏩", callback_data=f"next_{year}_{month}"),
    ]
    return buttons


def generate_weekdays_row() -> list[InlineKeyboardButton]:
    """
    Generates the row with abbreviated weekday names in Russian.

    Returns:
    - list[InlineKeyboardButton]: A list of weekday name buttons, Monday to Sunday.
    """
    buttons = [
        InlineKeyboardButton(text=day.name, callback_data="ignore") for day in DAYS_RU
    ]
    return buttons


def generate_month_days(year: int, month: int) -> list[list[InlineKeyboardButton]]:
    """
    Generates the grid of day buttons for the given month and year.

    Each week is represented as a list of buttons.
    The current day is marked with a bot-feature emoji ("🐈‍⬛").
    Empty cells (days outside the current month) are shown as blank buttons and have 'ignore' callback.

    Args:
    - year (int): The year for the calendar.
    - month (int): The month for the calendar (1–12).

    Returns:
    - list[list[InlineKeyboardButton]]: A grid of buttons representing calendar weeks and days.
    """
    cal = calendar.Calendar().monthdayscalendar(year, month)
    today = date.today()
    days = [
        [
            InlineKeyboardButton(
                text=(
                    "🐈‍⬛"
                    if day > 0 and date(year, month, day) == today
                    else (f"{day}" if day > 0 else " ")
                ),
                callback_data=f"day_{year}_{month}_{day}" if day > 0 else "ignore",
            )
            for day in week
        ]
        for week in cal
    ]
    return days


def generate_calendar_footer() -> list[InlineKeyboardButton]:
    """
    Generates the footer row of the calendar with additional actions.

    Includes a reset button to return to the current month and a back button to the main menu.

    Returns:
    - list[InlineKeyboardButton]: A list of footer buttons.
    """
    footer = [
        InlineKeyboardButton(text="🔄 Заново", callback_data="reset_calendar"),
        back_to_main_button(),
    ]
    return footer


def build_calendar(year: int, month: int) -> InlineKeyboardMarkup:
    """
    Constructs a full inline calendar keyboard for the given year and month.
    Combines the header, weekdays row, day grid, and footer into a complete keyboard layout.

    Args:
    - year (int): The year to display.
    - month (int): The month to display (1–12).

    Returns:
    - InlineKeyboardMarkup: The complete calendar as an inline keyboard markup.
    """
    keyboard = [generate_calendar_header(year, month), generate_weekdays_row()]
    keyboard.extend(generate_month_days(year, month))
    keyboard.append(generate_calendar_footer())
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


# @router_name.callback_query(F.data.startswith("day_"))     decorator to handle day selection
