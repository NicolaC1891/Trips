from aiogram import Router
from aiogram.types import CallbackQuery

from app.application.usecases.business_flow.dto import FlowStepRequestDTO
from app.application.usecases.business_flow.usecases import FetchFlowStepUseCase
from app.infra.logs.logger import log_user
from app.infra.rel_db.session_factory import async_session_factory
from app.infra.repositories.business_flow_r import FlowRepo
from app.ui.keyboards.business_flow.flow_step_kb_builder import FlowStepUIBuilder

router = Router()


async def handle_flow_step(callback: CallbackQuery):
    await callback.answer()

    prefix = callback.data.split("_", 1)[0]
    step_key = callback.data
    user_id = callback.from_user.id

    async with async_session_factory() as session:
        await log_user(user_id, prefix, session)
        repo = FlowRepo(session)
        input_dto = FlowStepRequestDTO(flow_prefix=prefix, step_key=step_key)
        use_case = FetchFlowStepUseCase(repo=repo, dto=input_dto)
        step = await use_case()

    reply = step.response
    keyboard = FlowStepUIBuilder(step).build_kb()
    await callback.message.edit_text(text=reply, reply_markup=keyboard)

