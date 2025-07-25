from aiogram.types import CallbackQuery

from app.application.usecases.office_cat.dto import OfficeCatRequestDTO
from app.application.usecases.office_cat.show_office_cat import ShowOfficeCatUseCase
from app.infra.repositories.menu_item_r import MenuItemRepo
from app.ui.keyboards.menu.kb_builders import SimpleMenuUIBuilder
from app.infra.repositories.cat_wisdom_r import CatWisdomRepo
from app.infra.rel_db.session_factory import async_session_factory


async def handle_show_office_cat(callback: CallbackQuery):
    await callback.answer()

    async with async_session_factory() as session:
        wisdom_repo = CatWisdomRepo(session)
        menu_item_repo = MenuItemRepo(session)
        input_dto = OfficeCatRequestDTO(response_key=callback.data)
        use_case = ShowOfficeCatUseCase(wisdom_repo, menu_item_repo, input_dto)
        output_dto = await use_case()

    reply = output_dto.reply
    keyboard = SimpleMenuUIBuilder().build_kb()
    await callback.message.edit_text(text=reply, reply_markup=keyboard)
