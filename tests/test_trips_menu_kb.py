from aiogram.types import InlineKeyboardMarkup

from main_menu.keyboards_menu import back_to_main_keyboard, main_menu_keyboard


def test_main_menu_keyboard():
    kb = main_menu_keyboard()
    menu_rows = kb.inline_keyboard
    expected_callback = [
        "home_travel",
        "abroad_travel",
        "my_calendar",
        "manual",
        "help",
        "cat_bot",
    ]
    actual_callback = [button.callback_data for row in menu_rows for button in row]
    assert isinstance(kb, InlineKeyboardMarkup)
    assert expected_callback == actual_callback


def test_back_to_main_keyboard():
    kb = back_to_main_keyboard()
    menu_rows = kb.inline_keyboard
    assert isinstance(kb, InlineKeyboardMarkup)
    assert len(menu_rows) == 1
