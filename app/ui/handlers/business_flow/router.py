from aiogram import Router

from app.ui.handlers.business_flow.handlers import handle_flow_step

router = Router()

router.callback_query(lambda c: c.data.startswith(("home_", "abroad_")))(handle_flow_step)
