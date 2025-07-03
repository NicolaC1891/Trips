from aiogram.types import InlineKeyboardButton
from keyboards.button_factory import back_to_main_button, back_button, forward_button, upward_button, options_button


def test_back_to_main_button():
    button = back_to_main_button()
    assert isinstance(button, InlineKeyboardButton), "Must return InlineKeyboardButton"
    assert button.text == '🏠 Главное меню', 'Must have this text (design issue)'
    assert button.callback_data == 'to_main', 'Must be to_main (DB relation)'


def test_back_button():
    button = back_button(callback_data='some_callback')
    assert isinstance(button, InlineKeyboardButton), "Must return InlineKeyboardButton"
    assert button.text == '⬅ Назад', 'Must have this text (design issue)'
    assert isinstance (button.callback_data, str), 'Must be string'


def test_forward_button():
    button = forward_button(callback_data='some_callback')
    assert isinstance(button, InlineKeyboardButton), "Must return InlineKeyboardButton"
    assert button.text == '➡ Дальше', 'Must have this text (design issue)'
    assert isinstance (button.callback_data, str), 'Must be string'


def test_upward_button():
    button = upward_button(text='some_text', callback_data='some_callback')
    assert isinstance(button, InlineKeyboardButton), "Must return InlineKeyboardButton"
    assert isinstance(button.text, str), 'Must be string (inbound argument)'
    assert isinstance(button.callback_data, str), 'Must be string'


def test_options_button():
    button = options_button(text='some_text', callback_data='some_callback')
    assert isinstance(button, InlineKeyboardButton), "Must return InlineKeyboardButton"
    assert isinstance(button.text, str), 'Must be string (inbound argument)'
    assert isinstance(button.callback_data, str), 'Must be string'