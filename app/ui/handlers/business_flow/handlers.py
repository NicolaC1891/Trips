from aiogram import Router
from aiogram.types import CallbackQuery

from app.application.usecases.business_flow.dto import FlowStepRequestDTO
from app.application.usecases.business_flow.usecases import FetchFlowStepUseCase
from app.infra.rel_db.session_factory import async_session_factory
from app.application.entities.flow_step_entity import FlowStepValidator
from app.infra.repositories.business_flow_r import FlowRepo
from app.ui.keyboards.business_flow.flow_step_kb_builder import FlowStepUIBuilder

router = Router()


async def handle_flow_step(callback: CallbackQuery):
    await callback.answer()

    prefix = callback.data.split("_", 1)[0]
    step_key = callback.data

    async with async_session_factory() as session:
        repo = FlowRepo(session)
        validator = FlowStepValidator()
        input_dto = FlowStepRequestDTO(flow_prefix=prefix, step_key=step_key)
        use_case = FetchFlowStepUseCase(repo=repo, validator=validator, dto=input_dto)
        output_dto = await use_case()

    step = output_dto.flow_step
    child_labels = output_dto.child_labels
    reply = output_dto.reply

    keyboard = FlowStepUIBuilder(child_labels, step).build_kb()
    await callback.message.edit_text(text=reply, reply_markup=keyboard)

