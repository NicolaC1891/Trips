from aiogram import Router, F
from aiogram.types import CallbackQuery

router = Router()


@router.callback_query(F.data == 'ignore')
async def ignore_callback(callback_query: CallbackQuery):
    await callback_query.answer()


@router.callback_query()
async def unknown_callback(callback_query: CallbackQuery):
    await callback_query.answer("Неизвестная команда или кнопка.", show_alert=True)

