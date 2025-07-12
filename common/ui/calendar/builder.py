from datetime import date
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from common.ui.calendar.locale_RU import MONTHS_RU, DAYS_RU


class CalendarUIBuilder:
    PREV_BTN = '⏪'
    NEXT_BTN = '⏩'
    RESET_BTN = '🔄  Сегодня'
    TODAY_BTN = "🐈‍⬛"
    TO_MAIN_BTN = '🏠  В меню'

    def __init__(self, feature_name, year, month, days):
        self.feature = feature_name
        self.year = year
        self.month = month
        self.days = days
        self.today = date.today()

    def _is_today(self, day: int) -> bool:
        if day == 0:
            return False
        return date(self.year, self.month, day) == self.today

    def _make_header(self) -> list[InlineKeyboardButton]:
        header = [
            InlineKeyboardButton(text=self.PREV_BTN, callback_data=f"{self.feature}_prev_{self.year}_{self.month}"),
            InlineKeyboardButton(text=f"{MONTHS_RU[self.month]} {self.year}", callback_data="ignore"),
            InlineKeyboardButton(text=self.NEXT_BTN, callback_data=f"{self.feature}_next_{self.year}_{self.month}"),
            ]
        return header

    @staticmethod
    def _make_weekdays() -> list[InlineKeyboardButton]:
        weekdays_block = [InlineKeyboardButton(text=f"{DAYS_RU[day]}", callback_data="ignore") for day in range(1, 8)]
        return weekdays_block

    def _make_days(self) -> list[list[InlineKeyboardButton]]:
        days_block = []
        for week in self.days:
            week_block = []
            for day in week:
                week_block.append(InlineKeyboardButton(text=f'{self.TODAY_BTN if self._is_today(day) else day if day > 0 else " "}',
                                                       callback_data=f'{self.feature}_day_{self.year}_{self.month}_{day}' if day > 0 else "ignore"))
            days_block.append(week_block)
        return days_block

    def _make_footer(self):
        footer = [
            InlineKeyboardButton(text=self.RESET_BTN, callback_data=f"{self.feature}_today_0_0"),
            InlineKeyboardButton(text=self.TO_MAIN_BTN, callback_data="to_main")
            ]
        return footer

    def build_calendar_keyboard(self):
        keyboard = []
        keyboard.append(self._make_header())
        keyboard.append(self._make_weekdays())
        keyboard.extend(self._make_days())
        keyboard.append(self._make_footer())
        markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
        return markup
