"""
Custom Keyboards for abroad trips menu

This module defines the structure and creation of inline keyboards used for the abroad trips functionality.
The keyboards are organized based on the various steps of the trip process, such as:
- Preparation
- Trip request
- Trip order
- In-trip info
- Report generation
- Navigation between various levels of the trip process

The following keyboards are created:
1. Main menu for abroad trips (`home_menu_kb`)
2. Trip request submenu (`home_memo_kb`)
3. Report generation submenu (`home_report_kb`)
4. Navigation keyboards for specific sections of the trip process

Each function in this module returns an `InlineKeyboardMarkup` object.

These keyboards are used in the bot interface to help users navigate through the abroad trip flow.
"""

from aiogram.types import InlineKeyboardMarkup

from common.buttons import (back_button, back_to_main_button, forward_button,
                            options_button, upward_button)


def build_abroad_menu_kb() -> InlineKeyboardMarkup:
    """
    Creates the main menu keyboard for abroad trips.

    This menu includes options such as:
       - Start with...
       - Apply for trip
       - Draw order
       - In-trip information
       - Advance report

    Returns:
    - InlineKeyboardMarkup object with main menu options.
    """
    abroad_menu = InlineKeyboardMarkup(
        inline_keyboard=[
            [options_button(text="1. С чего начать", callback_data="abroad_module")],
            [
                options_button(
                    text="2. Оформление докладной", callback_data="abroad_memo"
                )
            ],
            [
                options_button(
                    text="3. Оформление приказа", callback_data="abroad_order"
                )
            ],
            [options_button(text="4. В поездке", callback_data="abroad_trip")],
            [options_button(text="5. Авансовый отчет", callback_data="abroad_report")],
            [back_to_main_button()],
        ]
    )
    return abroad_menu


def build_abroad_memo_kb() -> InlineKeyboardMarkup:
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
                    text="2.1. Карточка в модуле", callback_data="abroad_memo_fill"
                )
            ],
            [
                options_button(
                    text='2.2. Выгрузка в СЭД "Канцлер"', callback_data="abroad_memo_upload"
                )
            ],
            [
                options_button(
                    text='2.3. Докладная в СЭД "Канцлер"',
                    callback_data="abroad_memo_final",
                )
            ],
            [
                options_button(
                    text="2.4. Маршрут согласования",
                    callback_data="abroad_memo_approve",
                )
            ],
            [
                back_button(callback_data="abroad_module"),
                forward_button(callback_data="abroad_memo_fill"),
            ],
            [
                upward_button(text="🌍 Наверх", callback_data="abroad_travel"),
                back_to_main_button(),
            ],
        ]
    )
    return memo_menu


def build_abroad_report_kb() -> InlineKeyboardMarkup:
    """
    Creates the advance report menu for abroad trips.

    This menu includes options for generating reports:
       - PDF report
       - Paper report

    Returns:
    - InlineKeyboardMarkup object with report options.
    """

    report_menu = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                options_button(text="В PDF", callback_data="abroad_report_pdf"),
                options_button(text="На бумаге", callback_data="abroad_report_paper"),
            ],
            [back_button(callback_data="abroad_trip")],
            [
                upward_button(text="🌍  Наверх", callback_data="abroad_travel"),
                back_to_main_button(),
            ],
        ]
    )
    return report_menu


def build_abroad_options_kb(
    back: str = None,
    forward: str = None,
    upward: str = None,
    upward_callback: str = None,
) -> InlineKeyboardMarkup:
    """
    Creates a navigation keyboard for abroad trips menu options with customizable buttons.

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


abroad_menu_kb = build_abroad_menu_kb()

abroad_module_kb = build_abroad_options_kb(
    forward="abroad_memo", upward="🌍  Наверх", upward_callback="abroad_travel"
)

abroad_memo_kb = build_abroad_memo_kb()
abroad_memo_fill_kb = build_abroad_options_kb(
    back="abroad_module",
    forward="abroad_memo_upload",
    upward="⬆  Наверх",
    upward_callback="abroad_memo",
)
abroad_memo_upload_kb = build_abroad_options_kb(
    back="abroad_memo_fill",
    forward="abroad_memo_final",
    upward="⬆  Наверх",
    upward_callback="abroad_memo",
)
abroad_memo_finalize_kb = build_abroad_options_kb(
    back="abroad_memo_upload",
    forward="abroad_memo_approve",
    upward="⬆  Наверх",
    upward_callback="abroad_memo",
)
abroad_memo_approve_kb = build_abroad_options_kb(
    back="abroad_memo_final",
    forward="abroad_order",
    upward="⬆  Наверх",
    upward_callback="abroad_memo",
)

abroad_order_kb = build_abroad_options_kb(
    back="abroad_memo_approve",
    forward="abroad_trip",
    upward="🌍  Наверх",
    upward_callback="abroad_travel",
)

abroad_trip_kb = build_abroad_options_kb(
    back="abroad_order",
    forward="abroad_report",
    upward="🌍  Наверх",
    upward_callback="abroad_travel",
)

abroad_report_kb = build_abroad_report_kb()
abroad_report_pdf_kb = build_abroad_options_kb(
    upward="⬆  Наверх", upward_callback="abroad_report"
)
abroad_report_paper_kb = build_abroad_options_kb(
    upward="⬆  Наверх", upward_callback="abroad_report"
)
