"""
Factory of common navigation buttons
"""

from aiogram.types import InlineKeyboardButton


def back_to_main_button() -> InlineKeyboardButton:
    return InlineKeyboardButton(text=f"🏠  В меню", callback_data='to_main')


def back_button(callback_data) -> InlineKeyboardButton:
    return InlineKeyboardButton(text=f"⬅  Назад", callback_data=callback_data)


def forward_button(callback_data) -> InlineKeyboardButton:
    return InlineKeyboardButton(text=f"➡  Дальше", callback_data=callback_data)


def upward_button(text, callback_data) -> InlineKeyboardButton:
    return InlineKeyboardButton(text=text, callback_data=callback_data)


def options_button(text, callback_data) -> InlineKeyboardButton:
    return InlineKeyboardButton(text=text, callback_data=callback_data)