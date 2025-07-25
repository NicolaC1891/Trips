from aiogram.types import CallbackQuery

from app.application.usecases.menu.dto import ShowMenuItemRequestDTO
from app.application.usecases.menu.show_menu_item import ShowMenuItemUseCase
from app.infra.rel_db.session_factory import async_session_factory
from app.infra.repositories.menu_item_r import MenuItemRepo
from app.ui.keyboards.menu.kb_builders import SimpleMenuUIBuilder


async def handle_manual(callback: CallbackQuery):
    await callback.answer()

    async with async_session_factory() as session:
        repo = MenuItemRepo(session)
        input_dto = ShowMenuItemRequestDTO(response_key=callback.data)
        use_case = ShowMenuItemUseCase(repo, input_dto)
        output_dto = await use_case()

    reply = output_dto.reply
    keyboard = SimpleMenuUIBuilder().build_kb()
    await callback.message.edit_text(text=reply, reply_markup=keyboard)
