from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


inline_bel = InlineKeyboardMarkup(inline_keyboard=[
[InlineKeyboardButton(text=f"Оформить заявку", callback_data='request')],
[InlineKeyboardButton(text=f"Проживание/суточные", callback_data='allowance')],
[InlineKeyboardButton(text=f"В поездке", callback_data='on_trip')],
[InlineKeyboardButton(text=f"Авансовый отчет", callback_data='report')],
[InlineKeyboardButton(text=f"В главное меню", callback_data='start')]])


