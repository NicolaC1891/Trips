from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.infra.cache.fsm import FSMCache
from app.infra.logs.logger import log_user
from app.infra.rel_db.session_factory import async_session_factory

router = Router()


# Initialize feature, show regions
@router.callback_query(lambda c: c.data == "planner_start")
async def handle_show_regions_from(callback: CallbackQuery, state: FSMContext):
    prefix = "planner"
    user_id = callback.from_user.id
    fsm_cache = FSMCache(state)
    await fsm_cache.create(feature_name=prefix, data={})

    async with async_session_factory() as session:
        await log_user(user_id, prefix, session)
        repo = PlannerRepo(session)
        use_case = ShowRegionsUseCase(repo=repo)
        regions = await use_case()
    kb_callback = "region_from:"
    markup = show_regions_kb(kb_callback)

    await callback.message.edit_text("Выберите область, где находится город отправления:",
                         reply_markup=markup)


# Region selected, show cities
@router.callback_query(F.data.startswith("region_from:"))
async def handle_show_cities_from(callback: types.CallbackQuery, state: FSMContext):
    fsm_cache = FSMCache(state)
    region_key = callback.data.split(":")[1]
    await fsm_cache.update("planner", from_region=region_key)

    async with async_session_factory() as session:
        repo = PlannerRepo(session)
        use_case = ShowCitiesUseCase(repo=repo)
        cities = await use_case()
    kb_callback = "city_from:"
    markup = show_cities_kb(kb_callback)
    await callback.message.edit_text("Выберите город отправления:",
                         reply_markup=markup)


# City selected, show destination regions
@router.callback_query(F.data.startswith("city_from:"))
async def handle_show_regions_to(callback: types.CallbackQuery, state: FSMContext):
    fsm_cache = FSMCache(state)
    city_key = callback.data.split(":")[1]
    await fsm_cache.update("planner", from_city=city_key)

    async with async_session_factory() as session:
        repo = PlannerRepo(session)
        use_case = ShowRegionsUseCase(repo=repo)
        regions = await use_case()
    kb_callback = "region_to:"
    markup = show_regions_kb(kb_callback)
    await callback.message.edit_text("Выберите область, где находится город прибытия:",
                                     reply_markup=markup)


# Region selected, show destination cities
@router.callback_query(F.data.startswith("region_to:"))
async def handle_show_cities_to(callback: types.CallbackQuery, state: FSMContext):
    fsm_cache = FSMCache(state)
    region_key = callback.data.split(":")[1]
    await fsm_cache.update("planner", to_region=region_key)

    async with async_session_factory() as session:
        repo = PlannerRepo(session)
        use_case = ShowCitiesUseCase(repo=repo)
        cities = await use_case()
    kb_callback = "city_to:"
    markup = show_cities_kb(kb_callback)
    await callback.message.edit_text("Выберите город прибытия:",
                                     reply_markup=markup)


# Everything selected, show result
@router.callback_query(F.data.startswith("city_to:"))
async def handle_show_cities_to(callback: types.CallbackQuery, state: FSMContext):
    fsm_cache = FSMCache(state)
    city_key = callback.data.split(":")[1]
    await fsm_cache.update("planner", to_city=city_key)
    trip_data = await fsm_cache.read("planner")

    async with async_session_factory() as session:
        repo = PlannerRepo(session)
        use_case = ShowPlanUseCase(repo=repo)
        message = await use_case()
    markup = final_kb()
    await callback.message.edit_text(text=message, reply_markup=markup)
    await fsm_cache.delete("planner")
    