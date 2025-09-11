from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, message
from app.application.entities.user_entity import User
from app.application.usecases.business_flow.dto import FlowStepRequestDTO
from app.application.usecases.business_flow.usecases import FetchFlowStepUseCase
from app.application.usecases.office_cat.show_office_cat import ShowOfficeCatUseCase
from app.infra.rel_db.session_factory import async_session_factory
from app.infra.repositories.business_flow_r import FlowRepo
from app.infra.repositories.cat_wisdom_r import CatWisdomRepo
from app.ui.keyboards.business_flow.flow_step_kb_builder import FlowStepUIBuilder


async def handle_office_cat(callback: CallbackQuery):
    await callback.answer()

    prefix = "menu"
    step_key = "office_cat"

    async with async_session_factory() as session:
        message_repo = FlowRepo(session)
        wisdom_repo = CatWisdomRepo(session)
        input_dto = FlowStepRequestDTO(flow_prefix=prefix, step_key=step_key)
        use_case = ShowOfficeCatUseCase(message_repo=message_repo, wisdom_repo=wisdom_repo, dto=input_dto)
        step = await use_case()

    reply = step.response
    keyboard = FlowStepUIBuilder(step).build_kb()
    await callback.message.edit_text(text=reply, reply_markup=keyboard)