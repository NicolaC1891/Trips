from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.button_factory import options_button, back_to_main_button


def main_menu_keyboard():
    inline_main = InlineKeyboardMarkup(inline_keyboard=[
[options_button(f"🇧🇾 🇧🇾 🇧🇾 ПО БЕЛАРУСИ 🇧🇾 🇧🇾 🇧🇾", 'travel_bel')],
[options_button(f"🌍 🌍 🌍 ЗА ГРАНИЦУ 🌍 🌍 🌍", 'travel_rus')],
[options_button(f"💬 ЧАстые ВОпросы", 'faq')],
[options_button(f"ℹ️ Помощь", 'help'),
 options_button(f"🐈‍⬛ Обратная связь", 'feedback')]
])
    return inline_main


def back_to_main_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[[back_to_main_button()]])


main_menu_kb = main_menu_keyboard()
back_to_main_kb = back_to_main_keyboard()
