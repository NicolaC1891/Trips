import sentry_sdk
from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery

from app.application.usecases.calendar.navigate import navigate_calendar
from app.ui.keyboards.calendar.kb_builder import CalendarUIBuilder

router = Router()


@router.callback_query(F.data == "ignore")
async def ignore_callback(callback: CallbackQuery):
    await callback.answer()
    return


@router.callback_query(lambda c: c.data.split("_")[1].startswith(("caltoday", "calprev", "calnext")))
async def handle_navigate_calendar(callback: CallbackQuery):
    feature_name, action, year, month = callback.data.split("_")
    year, month = int(year), int(month)
    year, month, days = navigate_calendar(action, year, month)
    markup = CalendarUIBuilder(feature_name=feature_name, year=year, month=month, days=days).build_calendar_keyboard()
    try:
        await callback.message.edit_reply_markup(reply_markup=markup)
    except TelegramBadRequest as e:
        if "message is not modified" not in str(e):
            sentry_sdk.capture_exception(e)
            await callback.message.answer(
                "Произошла ошибка Telegram. Попробуйте позже."
            )
            return