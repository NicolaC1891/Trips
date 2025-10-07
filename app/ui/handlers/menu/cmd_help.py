from aiogram.types import Message

from app.application.usecases.business_flow.usecases import GetFlowStep
from app.infra.rel_db.session_factory import async_session_factory
from app.infra.repositories.business_flow_r import FlowRepo
from app.ui.keyboards.business_flow.flow_step_kb_builder import FlowStepUIBuilder


async def handle_cmd_help(message: Message):
    table_name = "menu"
    step_key = "menu_help"

    async with async_session_factory() as session:

        repo = FlowRepo(session)
        use_case = GetFlowStep(repo=repo, table_name=table_name, step_key=step_key)
        step = await use_case()

    reply = step.response
    keyboard = FlowStepUIBuilder(step).build_kb()
    await message.answer(text=reply, reply_markup=keyboard)
