from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class AdvanceReminderUIBuilder:
    @staticmethod
    def build_kb():
        keyboard = [
            [InlineKeyboardButton(text="✅ Создать напоминание", callback_data="adv_create_reminder")],
            [InlineKeyboardButton(text="✏️ Изменить дату приезда", callback_data="advance_today_0_0")],
            [InlineKeyboardButton(text="❌ Отказаться и выйти", callback_data="to_main")]
            ]

        markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
        return markup
