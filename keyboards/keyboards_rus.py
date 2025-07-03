"""
Custom keyboards for Rus trips menu
"""

from aiogram.types import InlineKeyboardMarkup
from keyboards.button_factory import back_button, forward_button, upward_button, back_to_main_button
from keyboards.button_factory import options_button


def rus_menu_keyboard() -> InlineKeyboardMarkup:
    rus_menu = InlineKeyboardMarkup(inline_keyboard=[
[options_button(text=f'1. С чего начать', callback_data='module_r')],
[options_button(text=f"2. Оформление докладной", callback_data='memo')],
[options_button(text=f"3. Оформление приказа", callback_data='order_r')],
[options_button(text=f"4. В поездке", callback_data='on_trip_r')],
[options_button(text=f"5. Авансовый отчет", callback_data='report_r')],
[back_to_main_button()]])
    return rus_menu


def memo_keyboard() -> InlineKeyboardMarkup:
    memo_menu = InlineKeyboardMarkup(inline_keyboard=[
[options_button(text=f"2.1. Докладная в модуле", callback_data='request_r')],
[options_button(text=f'2.2. Обработка докладной', callback_data='chancellor_r')],
[options_button(text=f'2.3. Докладная в СЭД "Канцлер"', callback_data='completion_r')],
[options_button(text=f'2.4. Маршрут согласования', callback_data='approval_r')],
[back_button(callback_data='module_r'), forward_button(callback_data='request_r')],
[upward_button(text=f"🌍 Наверх", callback_data='travel_rus'), back_to_main_button()]])
    return memo_menu


def report_r_keyboard() -> InlineKeyboardMarkup:
    report_r_menu = InlineKeyboardMarkup(inline_keyboard=[
        [options_button(text=f"В PDF", callback_data='report_r_pdf'),
         options_button(text=f"На бумаге", callback_data='report_r_paper')],
        [back_button(callback_data='on_trip_r')],
        [upward_button(text=f"🌍  Наверх", callback_data='travel_rus'), back_to_main_button()]
    ])
    return report_r_menu


def rus_options_kb(back: str = None, forward: str = None, upward: str = None, upward_callback: str = None) -> InlineKeyboardMarkup:
    """
    Factory of navigation keyboards for menu options
    :param back: callback to previous message in business logic process
    :param forward: callback to next message in business logic process
    :param upward: button text depending on menu level
    :param upward_callback: callback to upper level menu
    :return:
    """
    rus_options = []
    row_1 = []
    if back:
        row_1.append(back_button(back))
    if forward:
        row_1.append(forward_button(forward))
    if row_1:
        rus_options.append(row_1)

    row_2 = []
    if upward:
        row_2.append(upward_button(upward, upward_callback))
    row_2.append(back_to_main_button())
    rus_options.append(row_2)

    return InlineKeyboardMarkup(inline_keyboard=rus_options)


rus_menu_kb = rus_menu_keyboard()
memo_kb = memo_keyboard()

module_r_kb = rus_options_kb(forward='memo', upward=f"🌍  Наверх", upward_callback='travel_rus')
form_r_kb = rus_options_kb(back='module_r', forward='chancellor_r', upward=f"⬆  Наверх", upward_callback='memo')
output_r_kb = rus_options_kb(back='request_r', forward='completion_r', upward=f"⬆  Наверх", upward_callback='memo')
completion_r_kb = rus_options_kb(back='chancellor_r', forward='approval_r', upward=f"⬆  Наверх", upward_callback='memo')
approval_r_kb = rus_options_kb(back='completion_r', forward='order_r', upward=f"⬆  Наверх", upward_callback='memo')
order_r_kb = rus_options_kb(back='approval_r', forward='on_trip_r', upward=f"🌍  Наверх", upward_callback='travel_rus')
trip_r_kb = rus_options_kb(back='order_r', forward='report_r', upward=f"🌍  Наверх", upward_callback='travel_rus')

report_r_kb = report_r_keyboard()
report_r_pdf_kb = rus_options_kb(upward=f"⬆  Наверх", upward_callback='report_r')
report_r_paper_kb = rus_options_kb(upward=f"⬆  Наверх", upward_callback='report_r')
