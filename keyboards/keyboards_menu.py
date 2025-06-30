from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


inline_main = InlineKeyboardMarkup(inline_keyboard=[
[InlineKeyboardButton(text=f"🇧🇾 🇧🇾 🇧🇾 По Беларуси 🇧🇾 🇧🇾 🇧🇾", parse_mode='HTML', callback_data='travel_bel')],
[InlineKeyboardButton(text=f"🇷🇺 🇷🇺 🇷🇺 За границу 🇷🇺 🇷🇺 🇷🇺", callback_data='travel_rus')],
[InlineKeyboardButton(text=f"❓ ЧАстые ВОпросы", callback_data='faq')],
[InlineKeyboardButton(text=f"👍 Что умеет бот", callback_data='can_do'),
InlineKeyboardButton(text=f"🐈‍⬛ Обратная связь", callback_data='feedback')]
])

feedback = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=f"В главное меню", callback_data='start')]])
can_do = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=f"В главное меню", callback_data='start')]])
faq = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=f"В главное меню", callback_data='start')]])

travel_bel = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=f"В главное меню", callback_data='start')]])

















