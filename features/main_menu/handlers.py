from aiogram import Router, F
from aiogram.filters import CommandStart, CommandObject, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from common.ui.builders import SimpleMenuUIBuilder
from features.main_menu.use_cases import ShowMainMenuUseCase, ShowHelp
from infrastructure.database.session import async_session_factory
from domain.models import User
from common.repos.instruction_repo import InstructionRepo
from common.logger.logger import logger
from features.main_menu.ui import MainMenuUIBuilder

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, command: CommandObject, state: FSMContext):
    await state.clear()

    async with async_session_factory() as session:
        tg_user = User(id=message.from_user.id, username=message.from_user.username, full_name=message.from_user.full_name)
        repo = InstructionRepo(session)
        use_case = ShowMainMenuUseCase(tg_user, repo)
        response = await use_case.execute()

    if command.args == "go":
        logger.info(f"User {tg_user.username} entered via QR code, link /start go")

    keyboard = MainMenuUIBuilder().build_main_menu_keyboard()

    await message.answer(text=response, reply_markup=keyboard)


@router.message(Command("help"))
async def cmd_help(message: Message):
    response_key = 'help'
    async with async_session_factory() as session:
        repo = InstructionRepo(session)
        use_case = ShowHelp(repo, response_key)
        response_message = await use_case.execute()
    keyboard = SimpleMenuUIBuilder().build_to_main_keyboard()
    await message.answer(text=response_message, reply_markup=keyboard)


@router.callback_query(F.data == "help")
async def handle_help(callback: CallbackQuery):
    response_key = 'help'
    async with async_session_factory() as session:
        repo = InstructionRepo(session)
        use_case = ShowHelp(repo, response_key)
        response_message = await use_case.execute()
    keyboard = SimpleMenuUIBuilder().build_to_main_keyboard()
    await callback.message.edit_text(text=response_message, reply_markup=keyboard)


@router.callback_query(F.data == "manual")
async def handle_manual(callback: CallbackQuery):
    response_key = 'manual'
    async with async_session_factory() as session:
        repo = InstructionRepo(session)
        use_case = ShowHelp(repo, response_key)
        response_message = await use_case.execute()
    keyboard = SimpleMenuUIBuilder().build_to_main_keyboard()
    await callback.message.edit_text(text=response_message, reply_markup=keyboard)



@router.callback_query(F.data == 'to_main')
async def handle_to_main(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()

    async with async_session_factory() as session:
        tg_user = User(id=callback.from_user.id, username=callback.from_user.username, full_name=callback.from_user.full_name)
        repo = InstructionRepo(session)
        use_case = ShowMainMenuUseCase(tg_user, repo)
        response = await use_case.execute()

    keyboard = MainMenuUIBuilder().build_main_menu_keyboard()

    await callback.message.edit_text(text=response, reply_markup=keyboard)



