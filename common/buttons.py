"""
Factory of common navigation buttons
"""

from aiogram.types import InlineKeyboardButton


def back_to_main_button() -> InlineKeyboardButton:
    """
    Creates a button that navigates back to the main menu.

    Returns:
    - InlineKeyboardButton: An inline keyboard button with UI text and callback.
    """
    return InlineKeyboardButton(text="🏠  В меню", callback_data="to_main")


def back_button(callback_data) -> InlineKeyboardButton:
    """
    Creates a back button with the specified callback data.

    Args:
    - callback_data (str): The callback data that will be sent when the button is pressed.

    Returns:
    - InlineKeyboardButton: An inline keyboard button with UI text and callback.
    """
    return InlineKeyboardButton(text="⬅  Назад", callback_data=callback_data)


def forward_button(callback_data) -> InlineKeyboardButton:
    """
    Creates a forward button with the specified callback data.

    Args:
    - callback_data (str): The callback data that will be sent when the button is pressed.

    Returns:
    - InlineKeyboardButton: An inline keyboard button with UI text and callback.
    """
    return InlineKeyboardButton(text="➡  Дальше", callback_data=callback_data)


def upward_button(text, callback_data) -> InlineKeyboardButton:
    """
    Creates an upward button with the specified callback data.

    Args:
    - callback_data (str): The callback data that will be sent when the button is pressed.

    Returns:
    - InlineKeyboardButton: An inline keyboard button with UI text and callback.
    """
    return InlineKeyboardButton(text=text, callback_data=callback_data)


def options_button(text, callback_data) -> InlineKeyboardButton:
    """
    Creates a button for an option with the specified text and callback data.
    Args:
    - text (str): The text to display on the button.
    - callback_data (str): The callback data that will be sent when the button is pressed.

    Returns:
    - InlineKeyboardButton: An inline keyboard button with the given text and callback data.
    """
    return InlineKeyboardButton(text=text, callback_data=callback_data)
