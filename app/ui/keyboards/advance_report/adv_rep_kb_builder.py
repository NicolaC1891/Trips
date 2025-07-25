from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class AdvanceReminderCreateUI:
    @staticmethod
    def build_kb() -> InlineKeyboardMarkup:
        keyboard = [
            [
                InlineKeyboardButton(
                    text="✅  Создать напоминание", callback_data="adv_create_reminder"
                )
            ],
            [
                InlineKeyboardButton(
                    text="✏️  Изменить дату приезда", callback_data="advance_today_0_0"
                )
            ],
            [InlineKeyboardButton(text="🏠  В меню", callback_data="to_main")],
        ]

        markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
        return markup


class AdvanceReminderExitUI:
    @staticmethod
    def build_kb() -> InlineKeyboardMarkup:
        keyboard = [
            [
                InlineKeyboardButton(
                    text="✏️  Другая командировка", callback_data="advance_today_0_0"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🏠  В меню", callback_data="to_main"
                )
            ],
        ]

        markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
        return markup


class AdvanceReminderMessageUI:
    def __init__(self, callback_key):
        self.callback_key = callback_key

    def build_kb(self) -> InlineKeyboardMarkup:
        keyboard = [
            [
                InlineKeyboardButton(text="Я уже отчитался!", callback_data=f"advance_del_{self.callback_key}"),
                InlineKeyboardButton(text="Напомни завтра", callback_data="to_main"),
            ],
            [
                InlineKeyboardButton(
                    text="Как оформить отчет", callback_data="home_4"
                )
            ],
        ]

        markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
        return markup
