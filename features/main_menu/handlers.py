import sentry_sdk
from aiogram import Router, F
from aiogram.filters import CommandStart, CommandObject, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from domain.user_entity import User
from features.main_menu.use_cases import (
    ShowMainMenuUseCase,
    ShowSimpleMenuOptionUseCase,
)
from infrastructure.database.session import async_session_factory
from features.business_trips.flow_repo import FlowRepo
from common.logger.logger import logger
from features.main_menu.ui import MainMenuUIBuilder, SimpleMenuUIBuilder

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, command: CommandObject, state: FSMContext):
    logger.info(f"User {message.from_user.username} used /start")  # add statistic info

    if command.args == "go":
        logger.info(f"User {message.from_user.username} entered via QR code")

    await state.clear()  # Make exception for cache!

    try:
        async with async_session_factory() as session:
            tg_user = User(
                user_id=message.from_user.id,
                username=message.from_user.username,
                full_name=message.from_user.full_name,
            )
            repo = FlowRepo(session)
            use_case = ShowMainMenuUseCase(tg_user, repo)
            reply = await use_case.execute()
        keyboard = MainMenuUIBuilder().build_kb()
        await message.answer(text=reply, reply_markup=keyboard)

    except Exception as e:
        logger.exception("Error in /start handler")
        sentry_sdk.capture_exception(e)
        await message.answer("Произошла ошибка. Попробуйте позже.")


@router.message(Command("help"))
async def cmd_help(message: Message):
    response_key = "help"

    try:
        async with async_session_factory() as session:
            repo = FlowRepo(session)
            use_case = ShowSimpleMenuOptionUseCase(repo, response_key)
            reply = await use_case.execute()
        keyboard = SimpleMenuUIBuilder().build_kb()
        await message.answer(text=reply, reply_markup=keyboard)

    except Exception as e:
        logger.exception("Error in /help handler")
        sentry_sdk.capture_exception(e)
        await message.answer("Произошла ошибка. Попробуйте позже.")


@router.callback_query(F.data == "help")
async def handle_help(callback: CallbackQuery):
    await callback.answer()

    try:
        async with async_session_factory() as session:
            repo = FlowRepo(session)
            use_case = ShowSimpleMenuOptionUseCase(
                repo=repo, response_key=callback.data
            )
            reply = await use_case.execute()
        keyboard = SimpleMenuUIBuilder().build_kb()
        await callback.message.edit_text(text=reply, reply_markup=keyboard)

    except Exception as e:
        logger.exception("Error in help handler")
        sentry_sdk.capture_exception(e)
        await callback.message.answer("Произошла ошибка. Попробуйте позже.")


@router.callback_query(F.data == "manual")
async def handle_manual(callback: CallbackQuery):
    await callback.answer()

    try:
        async with async_session_factory() as session:
            repo = FlowRepo(session)
            use_case = ShowSimpleMenuOptionUseCase(
                repo=repo, response_key=callback.data
            )
            reply = await use_case.execute()
        keyboard = SimpleMenuUIBuilder().build_kb()
        await callback.message.edit_text(text=reply, reply_markup=keyboard)

    except Exception as e:
        logger.exception("Error in manual handler")
        sentry_sdk.capture_exception(e)
        await callback.message.answer("Произошла ошибка. Попробуйте позже.")
        return


@router.callback_query(F.data == "to_main")
async def handle_to_main(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()

    try:
        async with async_session_factory() as session:
            tg_user = User(
                user_id=callback.from_user.id,
                username=callback.from_user.username,
                full_name=callback.from_user.full_name,
            )
            repo = FlowRepo(session)
            use_case = ShowMainMenuUseCase(tg_user=tg_user, repo=repo)
            reply = await use_case.execute()
        keyboard = MainMenuUIBuilder().build_kb()
        await callback.message.edit_text(text=reply, reply_markup=keyboard)

    except Exception as e:
        logger.exception("Error in to_main handler")
        sentry_sdk.capture_exception(e)
        await callback.message.answer("Произошла ошибка. Попробуйте позже.")
        return
