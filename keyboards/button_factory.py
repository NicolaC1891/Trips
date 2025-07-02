from aiogram.types import InlineKeyboardButton


def back_to_main_button():
    return InlineKeyboardButton(text=f"🏠 Главное меню", callback_data='to_main')


def back_button(callback_data):
    return InlineKeyboardButton(text=f"⬅ Назад", callback_data=callback_data)


def forward_button(callback_data):
    return InlineKeyboardButton(text=f"➡ Дальше", callback_data=callback_data)


def upward_button(text, callback_data):
    return InlineKeyboardButton(text=text, callback_data=callback_data)


def options_button(text, callback_data):
    return InlineKeyboardButton(text=text, callback_data=callback_data)