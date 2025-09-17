from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, message
from app.application.entities.user_entity import User
from app.application.usecases.business_flow.dto import FlowStepRequestDTO
from app.application.usecases.business_flow.usecases import FetchFlowStepUseCase
from app.infra.rel_db.session_factory import async_session_factory
from app.infra.repositories.business_flow_r import FlowRepo
from app.ui.keyboards.menu.kb_builders import MainMenuUIBuilder


async def handle_to_main(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()  # Make exception for cache!

    prefix = "menu"
    step_key = "to_main"

    async with async_session_factory() as session:
        tg_user = User(
            user_id=callback.from_user.id,
            username=callback.from_user.username,
            full_name=callback.from_user.full_name,
        )
        repo = FlowRepo(session)
        input_dto = FlowStepRequestDTO(flow_prefix=prefix, step_key=step_key)
        use_case = FetchFlowStepUseCase(repo=repo, dto=input_dto)
        step = await use_case()

    username = tg_user.full_name or "коллега"
    reply = step.response.format(username=username)
    keyboard = MainMenuUIBuilder.build_kb()
    await callback.message.edit_text(text=reply, reply_markup=keyboard)
