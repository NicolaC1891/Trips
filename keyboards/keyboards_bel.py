"""
Custom keyboards for Bel trips menu
"""

from aiogram.types import InlineKeyboardMarkup
from keyboards.button_factory import back_button, forward_button, upward_button, back_to_main_button
from keyboards.button_factory import options_button


def bel_menu_keyboard():
    bel_menu = InlineKeyboardMarkup(inline_keyboard=[
[options_button(text=f'1. С чего начать', callback_data='module')],
[options_button(text=f"2. Оформление заявки", callback_data='request_all')],
[options_button(text=f"3. Оформление приказа", callback_data='order')],
[options_button(text=f"4. В поездке", callback_data='on_trip')],
[options_button(text=f"5. Авансовый отчет", callback_data='report')],
[back_to_main_button()]])
    return bel_menu


def request_keyboard():
    request_menu = InlineKeyboardMarkup(inline_keyboard=[
[options_button(text=f"2.1. Заявка в модуле", callback_data='request')],
[options_button(text=f'2.2. Обработка заявки', callback_data='chancellor')],
[options_button(text=f'2.3. Заявка в СЭД "Канцлер"', callback_data='completion')],
[options_button(text=f'2.4. Маршрут согласования', callback_data='approval')],
[back_button(callback_data='module'), forward_button(callback_data='request')],
[upward_button(text=f"🇧🇾 Наверх", callback_data='travel_bel'), back_to_main_button()]])
    return request_menu


def report_keyboard():
    report_menu = InlineKeyboardMarkup(inline_keyboard=[
        [options_button(text=f"В PDF", callback_data='report_pdf'),
         options_button(text=f"На бумаге", callback_data='report_paper')],
        [back_button(callback_data='on_trip')],
        [upward_button(text=f"🇧🇾 Наверх", callback_data='travel_bel'), back_to_main_button()]
    ])
    return report_menu


def bel_options_kb(back=None, forward=None, upward=None, upward_callback=None):
    """
    Factory of navigation keyboards for menu options
    :param back: callback to previous message in business logic process
    :param forward: callback to next message in business logic process
    :param upward: button text depending on menu level
    :param upward_callback: callback to upper level menu
    :return:
    """

    bel_options = []
    row_1 = []
    if back:
        row_1.append(back_button(back))
    if forward:
        row_1.append(forward_button(forward))
    if row_1:
        bel_options.append(row_1)

    row_2 = []
    if upward:
        row_2.append(upward_button(upward, upward_callback))
    row_2.append(back_to_main_button())
    bel_options.append(row_2)

    return InlineKeyboardMarkup(inline_keyboard=bel_options)


bel_menu_kb = bel_menu_keyboard()
request_all_kb = request_keyboard()

module_kb = bel_options_kb(forward='request_all', upward=f"🇧🇾 Наверх", upward_callback='travel_bel')
form_kb = bel_options_kb(back='module', forward='chancellor', upward=f"⬆ Наверх", upward_callback='request_all')
output_kb = bel_options_kb(back='request', forward='completion', upward=f"⬆ Наверх", upward_callback='request_all')
completion_kb = bel_options_kb(back='chancellor', forward='approval', upward=f"⬆ Наверх", upward_callback='request_all')
approval_kb = bel_options_kb(back='completion', forward='order', upward=f"⬆ Наверх", upward_callback='request_all')
order_kb = bel_options_kb(back='approval', forward='on_trip', upward=f"🇧🇾 Наверх", upward_callback='travel_bel')
trip_kb = bel_options_kb(back='order', forward='report', upward=f"🇧🇾 Наверх", upward_callback='travel_bel')

report_kb = report_keyboard()
report_pdf_kb = bel_options_kb(upward=f"⬆ Наверх", upward_callback='report')
report_paper_kb = bel_options_kb(upward=f"⬆ Наверх", upward_callback='report')
