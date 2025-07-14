from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from features.main_menu.structure.menu_structure import BUSINESS_ITEMS, HELP_ITEMS


class MainMenuUIBuilder:
    @staticmethod
    def build_kb() -> InlineKeyboardMarkup:
        keyboard = []

        for item in BUSINESS_ITEMS:
            keyboard.append(
                [InlineKeyboardButton(text=item.label, callback_data=item.response_key)]
            )

        help_section = [
            InlineKeyboardButton(text=item.label, callback_data=item.response_key)
            for item in HELP_ITEMS
        ]
        keyboard.append(help_section)

        markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
        return markup



class SimpleMenuUIBuilder:
    BTN_MENU = "🏠  В меню"

    def build_kb(self) -> InlineKeyboardMarkup:
        keyboard = [[InlineKeyboardButton(text=self.BTN_MENU, callback_data="to_main")]]
        markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
        return markup