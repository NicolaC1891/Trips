from aiogram import Router
from aiogram.types import CallbackQuery

from app.application.usecases.business_flow.usecases import GetFlowStep
from app.infra.logs.logger import log_user
from app.infra.rel_db.session_factory import async_session_factory
from app.infra.repositories.business_flow_r import FlowRepo
from app.ui.keyboards.business_flow.flow_step_kb_builder import FlowStepUIBuilder

router = Router()


async def handle_flow_step(callback: CallbackQuery):
    await callback.answer()

    parts = callback.data.split("_", 2)
    table_name = parts[0]
    step_key = parts[0] + "_" + parts[1]
    options = parts[2] if len(parts) > 2 else None

    user_id = callback.from_user.id

    async with async_session_factory() as session:
        await log_user(user_id, step_key, session)
        await session.commit()

        repo = FlowRepo(session)
        use_case = GetFlowStep(repo=repo, table_name=table_name, step_key=step_key)
        step = await use_case()

    reply = step.response
    keyboard = FlowStepUIBuilder(step).build_kb()
    await callback.message.edit_text(text=reply, reply_markup=keyboard)

