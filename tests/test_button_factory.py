from aiogram.types import InlineKeyboardButton

from common.buttons import (back_button, back_to_main_button, forward_button,
                            options_button, upward_button)


def test_back_to_main_button():
    button = back_to_main_button()
    assert isinstance(button, InlineKeyboardButton)
    assert button.text == "🏠  В меню"
    assert button.callback_data == "to_main"


def test_back_button():
    button = back_button(callback_data="some_callback")
    assert isinstance(button, InlineKeyboardButton)
    assert button.text == "⬅  Назад"
    assert isinstance(button.callback_data, str)


def test_forward_button():
    button = forward_button(callback_data="some_callback")
    assert isinstance(button, InlineKeyboardButton)
    assert button.text == "➡  Дальше"
    assert isinstance(button.callback_data, str)


def test_upward_button():
    button = upward_button(text="some_text", callback_data="some_callback")
    assert isinstance(button, InlineKeyboardButton)
    assert isinstance(button.text, str)
    assert isinstance(button.callback_data, str)


def test_options_button():
    button = options_button(text="some_text", callback_data="some_callback")
    assert isinstance(button, InlineKeyboardButton)
    assert isinstance(button.text, str)
    assert isinstance(button.callback_data, str)
