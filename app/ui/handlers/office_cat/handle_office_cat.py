from aiogram.types import CallbackQuery

from app.application.usecases.business_flow.usecases import GetFlowStep
from app.application.usecases.office_cat.get_cat_wisdom import GetCatWisdom
from app.infra.logs.logger import log_user
from app.infra.rel_db.session_factory import async_session_factory
from app.infra.repositories.business_flow_r import FlowRepo
from app.infra.repositories.cat_wisdom_r import CatWisdomRepo
from app.ui.keyboards.business_flow.flow_step_kb_builder import FlowStepUIBuilder


async def handle_office_cat(callback: CallbackQuery):
    await callback.answer()

    table_name = "menu"
    step_key = "office_cat"
    user_id = callback.from_user.id

    async with async_session_factory() as session:
        await log_user(user_id, step_key, session)

        message_repo = FlowRepo(session)
        use_case = GetFlowStep(repo=message_repo, table_name=table_name, step_key=step_key)
        step = await use_case()

        wisdom_repo = CatWisdomRepo(session)
        use_case = GetCatWisdom(repo=wisdom_repo)
        wisdom = await use_case()

    reply = step.response.format(wisdom_text=wisdom)
    keyboard = FlowStepUIBuilder(step).build_kb()
    await callback.message.edit_text(text=reply, reply_markup=keyboard)
