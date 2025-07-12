from datetime import date

from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from common.fsm.fsm import FSMCache
from common.logger.logger import logger
from domain.models import User
from features.advance_report.exceptions import ReportDeadlinePassedError, ReminderTooLateError
from features.advance_report.ui import AdvanceReminderUIBuilder
from features.advance_report.usecases import AskTripArrivalDateUseCase, GetAdvanceReportDeadlineUseCase, CreateAdvanceReminder
from features.main_menu.ui import MainMenuUIBuilder
from features.main_menu.use_cases import ShowMainMenuUseCase
from infrastructure.database.session import async_session_factory
from common.repos.instruction_repo import InstructionRepo
from common.ui.calendar.builder import CalendarUIBuilder

router = Router()


@router.callback_query(lambda c: c.data.startswith(("advance_today", "advance_prev", "advance_next")))
async def handle_enter_advance_report(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await FSMCache(state).delete("advance_report")
    # parsing callback
    feature_name, prefix, year_str, month_str = callback.data.split("_")

    # getting done
    async with async_session_factory() as session:
        repo = InstructionRepo(session)
        use_case = AskTripArrivalDateUseCase(repo, prefix, year_str, month_str)  # may add DTO later
        message, year, month, days = await use_case.execute()

    keyboard = CalendarUIBuilder(feature_name, year, month, days).build_calendar_keyboard()
    try:    # Bypassing TG behavior with the same content and markup
        await callback.message.edit_text(text=message, reply_markup=keyboard)
    except TelegramBadRequest as e:
        if "message is not modified" not in str(e):
            raise


@router.callback_query(lambda c: c.data.startswith("advance_day"))
async def handle_choose_trip_return_date(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await FSMCache(state).delete("advance_report")
    # parsing callback
    _, _, year_str, month_str, day_str = callback.data.split("_")

    # getting done
    use_case = GetAdvanceReportDeadlineUseCase(year_str, month_str, day_str)  # may add DTO later
    return_date, reminder_date, report_deadline, message = await use_case.execute()
    await FSMCache(state).update("advance_report", return_date=return_date, reminder_date=reminder_date, report_deadline=report_deadline)

    keyboard = AdvanceReminderUIBuilder().build_kb()
    await callback.message.edit_text(text=message, reply_markup=keyboard)


@router.callback_query(lambda c: c.data == "adv_create_reminder")
async def handle_create_report_reminder(callback: CallbackQuery, state: FSMContext):
    all_data = await FSMCache(state).read("advance_report")
    user_id = callback.from_user.id
    return_date: date | None = all_data.get("return_date")
    reminder_date: date | None = all_data.get("reminder_date")
    report_deadline: date | None = all_data.get("report_deadline")
    keyboard = MainMenuUIBuilder().build_main_menu_keyboard()
    if not all([return_date, reminder_date, report_deadline]):
        logger.error("Creating report reminder: missing cached data")
        await callback.answer(text="Произошла ошибка. Выберите дату еще раз.", show_alert=True)
        return

    use_case = CreateAdvanceReminder(user_id, return_date, reminder_date, report_deadline)
    try:
        message = await use_case.execute()
        await callback.answer(message)
        async with async_session_factory() as session:
            tg_user = User(id=callback.from_user.id, username=callback.from_user.username,
                           full_name=callback.from_user.full_name)
            repo = InstructionRepo(session)
            use_case = ShowMainMenuUseCase(tg_user, repo)
            message = await use_case.execute()
            await FSMCache(state).delete("advance_report")
            await callback.message.edit_text(text=message, reply_markup=keyboard)
    except ReportDeadlinePassedError:
        await callback.answer("❌ Срок сдачи авансового отчета уже прошёл!", show_alert=True)
    except ReminderTooLateError:
        await callback.answer("⏰ Напоминание уже не актуально — пора сдавать отчет!", show_alert=True)
