from aiogram import Router
from aiogram.types import CallbackQuery, Message
from features.business_trips.usecases import FetchFlowStepUseCase
from infrastructure.database.session import async_session_factory
from domain.services_trips import TripsStepValidator
from common.repos.instruction_repo import InstructionRepo
from common.ui.builders import BusinessFlowStepUIBuilder

router = Router()


@router.callback_query(lambda c: c.data.startswith(("home_", "abroad_")))
async def handler_trips(callback_query: CallbackQuery):
    await callback_query.answer()
    prefix = callback_query.data.split("_", 1)[0]
    step_key = callback_query.data

    async with async_session_factory() as session:
        repo = InstructionRepo(session)
        validator = TripsStepValidator()
        use_case = FetchFlowStepUseCase(prefix, step_key, validator, repo)

        flow, step = await use_case.execute()

        response = step.content
        keyboard = BusinessFlowStepUIBuilder(flow, step).build_inline_keyboard()

        if isinstance(callback_query.message, Message):
            await callback_query.message.answer(text=response, reply_markup=keyboard)

