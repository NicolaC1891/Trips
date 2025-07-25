from aiogram.filters import CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.application.entities.user_entity import User
from app.application.usecases.menu.dto import ShowMenuItemRequestDTO
from app.application.usecases.menu.show_main_menu import ShowMainMenuUseCase
from app.infra.logs.logger import logger
from app.infra.rel_db.session_factory import async_session_factory
from app.infra.repositories.business_flow_r import FlowRepo
from app.infra.repositories.menu_item_r import MenuItemRepo
from app.ui.keyboards.menu.kb_builders import MainMenuUIBuilder


async def handle_cmd_start(message: Message, command: CommandObject, state: FSMContext):
    logger.info(f"User {message.from_user.username} used /start")  # add statistic info

    if command.args == "go":
        logger.info(f"User {message.from_user.username} entered via QR code")

    await state.clear()  # Make exception for cache!

    async with async_session_factory() as session:
        tg_user = User(
            user_id=message.from_user.id,
            username=message.from_user.username,
            full_name=message.from_user.full_name,
        )

        repo = MenuItemRepo(session)
        input_dto = ShowMenuItemRequestDTO(response_key='to_main')
        use_case = ShowMainMenuUseCase(tg_user, repo, input_dto)
        output_dto = await use_case()

    reply = output_dto.reply
    keyboard = MainMenuUIBuilder().build_kb()
    await message.answer(text=reply, reply_markup=keyboard)