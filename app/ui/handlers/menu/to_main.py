from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app.application.entities.user_entity import User
from app.application.usecases.menu.dto import ShowMenuItemRequestDTO
from app.application.usecases.menu.show_main_menu import ShowMainMenuUseCase
from app.infra.rel_db.session_factory import async_session_factory
from app.infra.repositories.menu_item_r import MenuItemRepo
from app.ui.keyboards.menu.kb_builders import MainMenuUIBuilder


async def handle_to_main(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()

    async with async_session_factory() as session:
        tg_user = User(
            user_id=callback.from_user.id,
            username=callback.from_user.username,
            full_name=callback.from_user.full_name,
        )

        repo = MenuItemRepo(session)
        input_dto = ShowMenuItemRequestDTO(response_key='to_main')
        use_case = ShowMainMenuUseCase(tg_user, repo, input_dto)
        output_dto = await use_case()

    reply = output_dto.reply
    keyboard = MainMenuUIBuilder().build_kb()
    await callback.message.edit_text(text=reply, reply_markup=keyboard)
