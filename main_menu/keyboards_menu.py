"""
Custom keyboards for the main menu.

This module defines reusable inline keyboards for the bot's main interface,
including the main menu and a back-to-main-menu button.

Functions:
- main_menu_keyboard(): Returns the inline keyboard for the main menu.
- back_to_main_keyboard(): Returns a single-button keyboard to go back to the main menu.

Exports:
- main_menu_kb: Prebuilt main menu keyboard.
- back_to_main_kb: Prebuilt back-to-main keyboard.
"""

from aiogram.types import InlineKeyboardMarkup

from common.buttons import back_to_main_button, options_button


def main_menu_keyboard():
    """
    Generates the inline keyboard for the main menu.

    The menu includes buttons for:
    - Travel in Belarus
    - Travel abroad
    - Advance report
    - Instructions
    - Feedback
    Options may be added or amended depending on the business logic.

    Returns:
    - InlineKeyboardMarkup: The main menu keyboard layout.
    """
    inline_main = InlineKeyboardMarkup(
        inline_keyboard=[
            [options_button("🇧🇾 🇧🇾 🇧🇾  ПО БЕЛАРУСИ  🇧🇾 🇧🇾 🇧🇾", "home_travel")],
            [options_button("🌍 🌍 🌍  ЗА ГРАНИЦУ  🌍 🌍 🌍", "abroad_travel")],
            [options_button("🔥 Авансовый отчет (beta)", "my_calendar")],
            [options_button("ℹ️  Как пользоваться ботом", "manual")],
            [
                options_button("🆘  Помощь", "help"),
                options_button("🐈‍⬛  Кот-бот", "cat_bot"),
            ],
        ]
    )
    return inline_main


def back_to_main_keyboard():
    """
    Generates a keyboard with a single 'Back to main menu' button.

    Returns:
    - InlineKeyboardMarkup: Inline keyboard with one navigation button.
    """
    return InlineKeyboardMarkup(inline_keyboard=[[back_to_main_button()]])


main_menu_kb = main_menu_keyboard()
back_to_main_kb = back_to_main_keyboard()
