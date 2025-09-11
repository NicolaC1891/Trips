from aiogram import Router
from aiogram.filters import CommandStart

from app.application.usecases.office_cat.handle_office_cat import handle_office_cat
from app.ui.handlers.menu.cmd_help import handle_cmd_help
from app.ui.handlers.menu.cmd_start import handle_cmd_start
from app.ui.handlers.menu.to_main import handle_to_main

router = Router()

router.message(CommandStart())(handle_cmd_start)
router.message(lambda m: m.text == "/help")(handle_cmd_help)
router.callback_query(lambda c: c.data == "to_main")(handle_to_main)
router.callback_query(lambda c: c.data == "office_cat")(handle_office_cat)
