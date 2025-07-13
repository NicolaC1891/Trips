from aiogram import Router, F
from aiogram.types import CallbackQuery

router = Router()


@router.callback_query(F.data == "ignore")
async def ignore_callback(callback: CallbackQuery):
    await callback.answer()
    return


@router.callback_query()
async def unknown_callback(callback: CallbackQuery):
    await callback.answer(
        'Неизвестная команда или кнопка. Напишите через "Идея!" - и бот станет лучше!',
        show_alert=True,
    )
    return
