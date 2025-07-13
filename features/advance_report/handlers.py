from datetime import date

import sentry_sdk
from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from common.fsm.fsm import FSMCache
from common.logger.logger import logger
from domain.user_entity import User
from features.advance_report.exceptions import ReportDeadlinePassedError, ReminderTooLateError, DuplicateReminderError
from features.advance_report.repo import ReminderRepo
from features.advance_report.ui import AdvanceReminderUIBuilder
from features.advance_report.usecases import AskTripArrivalDateUseCase, GetAdvanceReportDeadlineUseCase, CreateAdvanceReminder
from features.main_menu.ui import MainMenuUIBuilder
from features.main_menu.use_cases import ShowMainMenuUseCase
from infrastructure.database.session import async_session_factory
from common.repos.flow_repo import FlowRepo
from common.ui.calendar.kb_builder import CalendarUIBuilder

router = Router()


@router.callback_query(lambda c: c.data.startswith(("advance_today", "advance_prev", "advance_next")))
async def handle_enter_advance_report(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await FSMCache(state).delete("advance_report")

    feature_name, prefix, year_str, month_str = callback.data.split("_")

    try:
        async with async_session_factory() as session:
            repo = FlowRepo(session)
            use_case = AskTripArrivalDateUseCase(repo, prefix, year_str, month_str)  # add DTO later
            reply, year, month, days = await use_case.execute()
        keyboard = CalendarUIBuilder(feature_name, year, month, days).build_calendar_keyboard()

    except Exception as e:
        logger.exception("Error in enter advance report handler")
        sentry_sdk.capture_exception(e)
        await callback.message.answer("Произошла ошибка. Попробуйте позже.")
        return

    # Bypassing TG behavior with the same content and markup
    try:
        await callback.message.edit_text(text=reply, reply_markup=keyboard)
    except TelegramBadRequest as e:
        if "message is not modified" not in str(e):
            sentry_sdk.capture_exception(e)
            await callback.message.answer("Произошла ошибка Telegram. Попробуйте позже.")
            return


@router.callback_query(lambda c: c.data.startswith("advance_day"))
async def handle_choose_trip_return_date(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    _, _, year_str, month_str, day_str = callback.data.split("_")

    try:
        use_case = GetAdvanceReportDeadlineUseCase(year_str, month_str, day_str)  # may add DTO later
        return_date, reminder_date, report_deadline, reply = await use_case.execute()
        await FSMCache(state).update(
            feature_name="advance_report",
            return_date=return_date,
            reminder_date=reminder_date,
            report_deadline=report_deadline)
        keyboard = AdvanceReminderUIBuilder().build_kb()
        await callback.message.edit_text(text=reply, reply_markup=keyboard)

    except Exception as e:
        logger.exception("Error in choose trip return date handler")
        sentry_sdk.capture_exception(e)
        await callback.message.answer("Произошла ошибка. Выберите дату еще раз.")
        await FSMCache(state).delete("advance_report")
        return


@router.callback_query(lambda c: c.data == "adv_create_reminder")
async def handle_create_report_reminder(callback: CallbackQuery, state: FSMContext):

    # if user has created a reminder and presses Create again (but cache is empty)
    all_data = await FSMCache(state).read("advance_report")
    if not all_data:
        await callback.answer(text="Данные о дате не найдены. Пожалуйста, выберите дату заново.",show_alert=True)
        return

    return_date: date | None = all_data.get("return_date")
    reminder_date: date | None = all_data.get("reminder_date")
    report_deadline: date | None = all_data.get("report_deadline")

    # usual scenario, validating cache data
    if not all([return_date, reminder_date, report_deadline]):
        e = Exception("Error: missing cache data")
        logger.error(f"{e}")
        sentry_sdk.capture_exception(e)
        await callback.answer(text="Произошла ошибка. Выберите дату еще раз.", show_alert=True)
        await FSMCache(state).delete("advance_report")
        return

    today = date.today()

    if report_deadline < today:
        await callback.answer("❌ Срок сдачи авансового отчета уже прошёл!", show_alert=True)
        return

    if reminder_date == today:
        await callback.answer("⏰ Напоминание уже не актуально — пора сдавать отчет!", show_alert=True)
        return

    try:
        async with async_session_factory() as session:
            repo = ReminderRepo(session)
            use_case = CreateAdvanceReminder(
                repo=repo,
                user_id=callback.from_user.id,
                return_date=return_date,
                reminder_date=reminder_date,
                report_deadline=report_deadline
            )
            await use_case.execute()

    except DuplicateReminderError as e:
        logger.exception(f"{e}")
        sentry_sdk.capture_exception(e)
        await callback.answer("Такое напоминание уже существует", show_alert=True)
        return

    except Exception as e:
        logger.exception("Error creating advance report reminder")
        sentry_sdk.capture_exception(e)
        await callback.answer("Ошибка при создании напоминания", show_alert=True)
        return

    await FSMCache(state).delete("advance_report")
    await callback.answer("Напоминание создано!")
