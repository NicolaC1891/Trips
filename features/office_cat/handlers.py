import sentry_sdk
from aiogram import F, Router
from aiogram.types import CallbackQuery

from common.logger.logger import logger
from features.business_trips.flow_repo import FlowRepo
from features.business_trips.flow_menu_kb_builders import SimpleMenuUIBuilder
from features.office_cat.repo import CatWisdomRepo
from features.office_cat.use_cases import GetCatWisdomUseCase
from infrastructure.database.session import async_session_factory

router = Router()


@router.callback_query(F.data == "office_cat")
async def handle_cat_wisdom(callback: CallbackQuery):
    await callback.answer()

    try:
        async with async_session_factory() as session:
            wisdom_repo = CatWisdomRepo(session)
            message_repo = FlowRepo(session)
            use_case = GetCatWisdomUseCase(wisdom_repo, message_repo, callback.data)
            reply = await use_case.execute()
        keyboard = SimpleMenuUIBuilder().build_kb()
        if callback.message:
            await callback.message.edit_text(text=reply, reply_markup=keyboard)

    except Exception as e:
        logger.exception("Error in cat_wisdom handler")
        sentry_sdk.capture_exception(e)
        await callback.message.answer("Произошла ошибка. Попробуйте позже.")
        return
