from aiogram import Router

from app.ui.handlers.office_cat.show_office_cat import handle_show_office_cat

router = Router()

router.callback_query(lambda c: c.data == "office_cat")(handle_show_office_cat)
