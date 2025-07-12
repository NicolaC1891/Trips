from aiogram import F, Router
from aiogram.types import CallbackQuery

from common.repos.instruction_repo import InstructionRepo
from common.ui.builders import SimpleMenuUIBuilder
from features.office_cat.repo import CatWisdomRepo
from features.office_cat.use_cases import GetCatWisdomUseCase
from infrastructure.database.session import async_session_factory

router = Router()

@router.callback_query(F.data == "office_cat")
async def handle_cat_wisdom(callback_query: CallbackQuery):
    await callback_query.answer()
    response_key = 'office_cat'
    async with async_session_factory() as session:
        wisdom_repo = CatWisdomRepo(session)
        message_repo = InstructionRepo(session)
        use_case = GetCatWisdomUseCase(wisdom_repo, message_repo, response_key)
        message = await use_case.execute()
    keyboard = SimpleMenuUIBuilder().build_to_main_keyboard()
    await callback_query.message.edit_text(text=message, reply_markup=keyboard)
