from datetime import date

from aiogram import types, F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app.application.usecases.business_flow.usecases import GetFlowStep
from app.application.usecases.planner.planner_usecase import ShowCitiesUseCase, AskTripPlannedDateUseCase, ShowTripInfoUseCase
from app.infra.cache.fsm import FSMCache
from app.infra.logs.logger import log_user
from app.infra.rel_db.session_factory import async_session_factory
from app.infra.repositories.business_flow_r import FlowRepo
from app.infra.repositories.planner_r import PlannerRepo, OpenRouteService, OpenMeteoService
from app.ui.keyboards.calendar.kb_builder import CalendarUIBuilder
from app.ui.keyboards.planner_kb import make_region_kb, make_cities_kb, resulting_kb, final_kb

router = Router()


# Initialize feature, show regions
@router.callback_query(lambda c: c.data == "planner_start")
async def handle_show_regions_from(callback: CallbackQuery, state: FSMContext):
    fsm_cache = FSMCache(state)
    await FSMCache(state).delete("planner")
    await fsm_cache.create(feature_name="planner", data={})

    table_name = callback.data.split("_", 1)[0]
    step_key = callback.data
    user_id = callback.from_user.id

    async with async_session_factory() as session:
        await log_user(user_id, table_name, session)
        repo = FlowRepo(session)
        use_case = GetFlowStep(repo=repo, table_name=table_name, step_key=step_key)
        step = await use_case()
    reply = step.response

    kb_callback = "planner_from-region"
    markup = make_region_kb(direction=kb_callback)
    await callback.message.edit_text(text=reply, reply_markup=markup)


# Region selected, show cities
@router.callback_query(F.data.startswith("planner_from-region"))
async def handle_show_cities_from(callback: types.CallbackQuery, state: FSMContext):
    fsm_cache = FSMCache(state)
    flow_key, region_key = callback.data.split(":")
    prefix, step_key = flow_key.split("_")
    await fsm_cache.update("planner", from_region=region_key)

    async with async_session_factory() as session:
        repo = PlannerRepo(session)
        use_case = ShowCitiesUseCase(repo=repo, region=region_key)
        cities = await use_case()

        repo = FlowRepo(session)
        use_case = GetFlowStep(repo=repo, table_name=prefix, step_key=step_key)
        step = await use_case()

    kb_callback = "city_from"
    reply = step.response
    markup = make_cities_kb(cities, kb_callback)
    await callback.message.edit_text(text=reply, reply_markup=markup)


# City selected, show destination regions
@router.callback_query(F.data.startswith("city_from"))
async def handle_show_regions_to(callback: types.CallbackQuery, state: FSMContext):
    fsm_cache = FSMCache(state)
    city_key = callback.data.split(":")[1]
    await fsm_cache.update("planner", from_city=city_key)

    message = "Выберите область, где находится город прибытия"
    kb_callback = "region_to"
    markup = make_region_kb(direction=kb_callback)
    await callback.message.edit_text(text=message, reply_markup=markup)


# Region selected, show destination cities
@router.callback_query(F.data.startswith("region_to"))
async def handle_show_cities_to(callback: types.CallbackQuery, state: FSMContext):
    fsm_cache = FSMCache(state)
    region_key = callback.data.split(":")[1]
    await fsm_cache.update("planner", to_region=region_key)

    async with async_session_factory() as session:
        repo = PlannerRepo(session)
        use_case = ShowCitiesUseCase(repo=repo, region=region_key)
        cities = await use_case()
    kb_callback = "city_to"
    message = "Выберите город прибытия"
    markup = make_cities_kb(cities, kb_callback)
    await callback.message.edit_text(text=message, reply_markup=markup)


# Everything selected, show calendar, navigate calendar

@router.callback_query(lambda c: c.data.startswith(("city_to", "planner_today", "planner_prev", "planner_next")))
async def handle_show_calendar(callback: types.CallbackQuery, state: FSMContext):
    if callback.data.startswith("city_to"):
        fsm_cache = FSMCache(state)
        city_key = callback.data.split(":")[1]
        await fsm_cache.update("planner", to_city=city_key)

        message = "Выберите дату начала командировки"
        year, month, days = await AskTripPlannedDateUseCase("today", year_str="0", month_str="0").execute()
        markup = CalendarUIBuilder(feature_name="planner", year=year, month=month, days=days).build_calendar_keyboard()
        await callback.message.edit_text(text=message, reply_markup=markup)

    else:
        message = "Выберите дату начала командировки"
        feature_name, prefix, year, month = callback.data.split("_")

        year, month, days = await AskTripPlannedDateUseCase(prefix=prefix, year_str=year, month_str=month).execute()
        markup = CalendarUIBuilder(feature_name=feature_name, year=year, month=month, days=days).build_calendar_keyboard()
        await callback.message.edit_text(text=message, reply_markup=markup)
        try:
            message = "Выберите дату начала командировки"
            await callback.message.edit_text(text=message, reply_markup=markup)
        except TelegramBadRequest as e:
            if "message is not modified" not in str(e):
                await callback.message.answer(
                    "Произошла ошибка Telegram. Попробуйте позже."
                )
                return


# Showing resulting information, ask for core action
@router.callback_query(lambda c: c.data.startswith("planner_day"))
async def handle_choose_trip_planned_date(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    _, _, year_str, month_str, day_str = callback.data.split("_")
    selected_date = date(int(year_str), int(month_str), int(day_str))

#  добавить проверку прошлой даты
    fsm_cache = FSMCache(state)
    await fsm_cache.update(feature_name="planner", trip_date=selected_date)

    cache_data = await fsm_cache.read("planner")
    city_from = cache_data["from_city"]
    city_to = cache_data["to_city"]
    trip_date = cache_data["trip_date"]

    if trip_date < date.today():
        message = "Вы выбрали дату в прошлом. Выберите актуальную дату."
        markup = final_kb()
    else:
        message = (f"<b>Ваша командировка</b>\n\n"
                   f"Из города: <b>{city_from}</b>\n"
                   f"В город: <b>{city_to}</b>\n"
                   f"Дата поездки: <b>{trip_date.strftime("%d.%m.%Y")}</b>")
        markup = resulting_kb()
    await callback.message.edit_text(text=message, reply_markup=markup)


@router.callback_query(lambda c: c.data.startswith("planner_core"))
async def handle_planner_core(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    fsm_cache = FSMCache(state)
    cache_data = await fsm_cache.read("planner")
    city_from = cache_data["from_city"]
    city_to = cache_data["to_city"]
    trip_date = cache_data["trip_date"]

    async with async_session_factory() as session:
        repo = PlannerRepo(session)
        route_service = OpenRouteService()
        weather_service = OpenMeteoService()

        use_case = ShowTripInfoUseCase(
            repo=repo,
            route_service=route_service,
            weather_service=weather_service,
            city_from=city_from,
            city_to=city_to,
            trip_date=trip_date
        )

        message_route = await use_case.get_route()
        message_hotels = await use_case.get_hotels()
        message_weather = await use_case.get_weather()

    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(message_route)
    await callback.message.answer(message_hotels, disable_web_page_preview=True)
    await callback.message.answer(message_weather)

    final_message = "Желаете спланировать еще раз?"
    markup = final_kb()
    await callback.message.answer(text=final_message, reply_markup=markup)
