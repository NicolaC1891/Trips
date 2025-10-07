from datetime import date

import sentry_sdk
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app.application.usecases.business_flow.usecases import GetFlowStep
from app.application.usecases.calendar.navigate import get_calendar_days
from app.infra.cache.fsm import FSMCache
from app.infra.logs.logger import logger, log_user
from app.application.usecases.advance_report.exceptions import DuplicateReminderError
from app.infra.repositories.adv_rep_reminder_r import ReminderRepo
from app.ui.keyboards.advance_report.adv_rep_kb_builder import AdvanceReminderCreateUI, AdvanceReminderExitUI
from app.application.usecases.advance_report.usecases import (
    GetReportDeadline,
    CreateAdvanceReminder, DeleteAdvanceReminder)

from app.infra.rel_db.session_factory import async_session_factory
from app.infra.repositories.business_flow_r import FlowRepo
from app.ui.keyboards.calendar.kb_builder import CalendarUIBuilder

router = Router()


@router.callback_query(lambda c: c.data == "advance_start")
async def handle_advance_start(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await FSMCache(state).delete("advance_report")

    parts = callback.data.split("_")
    table_name = parts[0]
    step_key = parts[0] + "_" + parts[1]
    user_id = callback.from_user.id

    async with async_session_factory() as session:
        await log_user(user_id, table_name, session)
        repo = FlowRepo(session)
        use_case = GetFlowStep(repo=repo, table_name=table_name, step_key=step_key)
        step = await use_case()

    message = step.response
    year = date.today().year
    month = date.today().month
    days = get_calendar_days(year, month)
    markup = CalendarUIBuilder(feature_name=table_name, year=year, month=month, days=days).build_calendar_keyboard()

    await callback.message.edit_text(text=message, reply_markup=markup)


@router.callback_query(lambda c: c.data.startswith("advance_day"))
async def handle_choose_trip_return_date(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    _, _, year_str, month_str, day_str = callback.data.split("_")

    try:
        use_case = GetReportDeadline(year_str, month_str, day_str)
        return_date, reminder_date, report_deadline, reply = await use_case.execute()
        await FSMCache(state).update(
            feature_name="advance_report",
            return_date=return_date,
            reminder_date=reminder_date,
            report_deadline=report_deadline,
        )
        keyboard = AdvanceReminderCreateUI().build_kb()
        await callback.message.edit_text(text=reply, reply_markup=keyboard)

    except Exception as e:
        logger.exception("Error in choose trip return date handler")
        sentry_sdk.capture_exception(e)
        await callback.message.answer("Произошла ошибка. Выберите дату еще раз.")
        await FSMCache(state).delete("advance_report")
        return


@router.callback_query(lambda c: c.data == "adv_create_reminder")
async def handle_create_report_reminder(callback: CallbackQuery, state: FSMContext):

    all_data = await FSMCache(state).read("advance_report")
    if not all_data:
        await callback.answer(
            text="Данные о дате не найдены. Пожалуйста, выберите дату заново.",
            show_alert=True,
        )
        return

    return_date: date | None = all_data.get("return_date")
    reminder_date: date | None = all_data.get("reminder_date")
    report_deadline: date | None = all_data.get("report_deadline")

    today = date.today()

    if report_deadline < today:
        await callback.answer(
            "❌ Срок сдачи авансового отчета уже прошёл!", show_alert=True
        )
        return

    if report_deadline == today:
        await callback.answer(
            "⏰ Напоминание уже не актуально — пора сдавать отчет!", show_alert=True
        )
        return

    try:
        async with async_session_factory() as session:
            repo = ReminderRepo(session)
            use_case = CreateAdvanceReminder(
                repo=repo,
                user_id=callback.from_user.id,
                return_date=return_date,
                reminder_date=reminder_date,
                report_deadline=report_deadline,
            )
            reply = await use_case.execute()
            keyboard = AdvanceReminderExitUI.build_kb()
            await callback.message.edit_text(text=reply, reply_markup=keyboard)

    except DuplicateReminderError as e:
        logger.exception(f"{e}")
        await callback.answer("Такое напоминание уже существует", show_alert=True)
        return

    except Exception as e:
        logger.exception("Error creating advance report reminder")
        sentry_sdk.capture_exception(e)
        await callback.answer("Ошибка при создании напоминания", show_alert=True)
        return

    await FSMCache(state).delete("advance_report")


@router.callback_query(lambda c: c.data.startswith("advance_del_"))
async def handle_delete_report_reminder(callback: CallbackQuery):
    required_date = callback.data.split("_", 2)[2]
    year, month, day = [int(num) for num in required_date.split("_")]
    user_id = callback.from_user.id
    return_date = date(year, month, day)
    async with async_session_factory() as session:
        repo = ReminderRepo(session)
        use_case = DeleteAdvanceReminder(repo, user_id, return_date)
        await use_case.execute()
        await callback.answer(text="Напоминание больше не активно")
