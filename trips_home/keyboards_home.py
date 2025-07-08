"""
Custom Keyboards for Belarusian trips menu

This module defines the structure and creation of inline keyboards used for the Belarusian trips functionality.
The keyboards are organized based on the various steps of the trip process, such as:
- Preparation
- Trip request
- Trip order
- In-trip info
- Report generation
- Navigation between various levels of the trip process

The following keyboards are created:
1. Main menu for Belarusian trips (`home_menu_kb`)
2. Trip request submenu (`home_memo_kb`)
3. Report generation submenu (`home_report_kb`)
4. Navigation keyboards for specific sections of the trip process

Each function in this module returns an `InlineKeyboardMarkup` object.

These keyboards are used in the bot interface to help users navigate through the Belarusian trip flow.
"""

from aiogram.types import InlineKeyboardMarkup

from common.buttons import (back_button, back_to_main_button, forward_button,
                            options_button, upward_button)


def build_home_menu_kb():
    """
    Creates the main menu keyboard for Belarusian trips.

    This menu includes options such as:
       - Start with...
       - Apply for trip
       - Draw order
       - In-trip information
       - Advance report

    Returns:
    - InlineKeyboardMarkup object with main menu options.
    """
    home_menu = InlineKeyboardMarkup(
        inline_keyboard=[
            [options_button(text="1. С чего начать", callback_data="home_module")],
            [options_button(text="2. Оформление заявки", callback_data="home_memo")],
            [options_button(text="3. Оформление приказа", callback_data="home_order")],
            [options_button(text="4. В поездке", callback_data="home_trip")],
            [options_button(text="5. Авансовый отчет", callback_data="home_report")],
            [back_to_main_button()],
        ]
    )
    return home_menu


def build_home_memo_kb():
    """
    Creates the menu for handling trip requests.

    This menu includes options such as:
       - Filling the request in the module
       - Upload the request to electronic document flow
       - Finalize the request
       - Approval route

    Returns:
    - InlineKeyboardMarkup object with trip request options.
    """
    memo_menu = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                options_button(
                    text="2.1. Заявка в модуле", callback_data="home_memo_fill"
                )
            ],
            [
                options_button(
                    text="2.2. Обработка заявки", callback_data="home_memo_upload"
                )
            ],
            [
                options_button(
                    text='2.3. Заявка в СЭД "Канцлер"', callback_data="home_memo_final"
                )
            ],
            [
                options_button(
                    text="2.4. Маршрут согласования", callback_data="home_memo_approve"
                )
            ],
            [
                back_button(callback_data="home_module"),
                forward_button(callback_data="home_memo_fill"),
            ],
            [
                upward_button(text="🇧🇾 Наверх", callback_data="home_travel"),
                back_to_main_button(),
            ],
        ]
    )
    return memo_menu


def build_home_report_kb():
    """
    Creates the advance report menu for Belarusian trips.

    This menu includes options for generating reports:
       - PDF report
       - Paper report

    Returns:
    - InlineKeyboardMarkup object with report options.
    """
    report_menu = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                options_button(text="В PDF", callback_data="home_report_pdf"),
                options_button(text="На бумаге", callback_data="home_report_paper"),
            ],
            [back_button(callback_data="home_trip")],
            [
                upward_button(text="🇧🇾 Наверх", callback_data="home_travel"),
                back_to_main_button(),
            ],
        ]
    )
    return report_menu


def build_home_options_kb(back=None, forward=None, upward=None, upward_callback=None):
    """
    Creates a navigation keyboard for Belarusian trips menu options with customizable buttons.

    This keyboard includes:
    - "Back" button (if `back` parameter is provided)
    - "Forward" button (if `forward` parameter is provided)
    - "Upward" button (if `upward` parameter is provided)
    - "Back to main menu" button

    Args:
    - back: Callback for the "Back" button (optional).
    - forward: Callback for the "Forward" button (optional).
    - upward: Text for the "Upward" button (optional).
    - upward_callback: Callback for the "Upward" button (optional).

    Returns:
    - InlineKeyboardMarkup object with navigation buttons.
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


home_menu_kb = build_home_menu_kb()

home_module_kb = build_home_options_kb(
    forward="home_memo", upward="🇧🇾 Наверх", upward_callback="home_travel"
)

home_memo_kb = build_home_memo_kb()
home_memo_fill_kb = build_home_options_kb(
    back="home_module",
    forward="home_memo_upload",
    upward="⬆ Наверх",
    upward_callback="home_memo",
)
home_memo_upload_kb = build_home_options_kb(
    back="home_memo_fill",
    forward="home_memo_final",
    upward="⬆ Наверх",
    upward_callback="home_memo",
)
home_memo_finalize_kb = build_home_options_kb(
    back="home_memo_upload",
    forward="home_memo_approve",
    upward="⬆ Наверх",
    upward_callback="home_memo",
)
home_memo_approve_kb = build_home_options_kb(
    back="home_memo_final",
    forward="home_order",
    upward="⬆ Наверх",
    upward_callback="home_memo",
)

home_order_kb = build_home_options_kb(
    back="home_memo_approve",
    forward="home_trip",
    upward="🇧🇾 Наверх",
    upward_callback="home_travel",
)

home_trip_kb = build_home_options_kb(
    back="home_order",
    forward="home_report",
    upward="🇧🇾 Наверх",
    upward_callback="home_travel",
)

home_report_kb = build_home_report_kb()
home_report_pdf_kb = build_home_options_kb(
    upward="⬆ Наверх", upward_callback="home_report"
)
home_report_paper_kb = build_home_options_kb(
    upward="⬆ Наверх", upward_callback="home_report"
)
