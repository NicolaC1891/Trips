from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart
import keyboards.keyboards_menu as kb
import keyboards.keyboards_bel as kb_bel
from aiogram.types import CallbackQuery

router_menu = Router()


@router_menu.message(CommandStart())
async def cmd_start(message: Message):
    user_name = message.from_user.full_name
    await message.answer(f"Здравствуйте, {user_name}!\n\n"
                         f"Какая командировка вас интересует?", reply_markup=kb.inline_main)


@router_menu.callback_query(F.data == 'feedback')
async def cmd_feedback(callback_query: CallbackQuery):
    await callback_query.answer('Вы запросили помощь')
    await callback_query.message.answer('Помощь в пути', reply_markup=kb.feedback)


@router_menu.callback_query(F.data == 'start')
async def cmd_back_to_main(callback_query: CallbackQuery):
    await callback_query.answer('Идем в начало')
    await callback_query.message.answer(f"Какая командировка вас интересует?", reply_markup=kb.inline_main)

@router_menu.callback_query(F.data == 'can_do')
async def cmd_can_do(callback_query: CallbackQuery):
    await callback_query.answer('Вам интересно, что я умею?')
    await callback_query.message.answer(f"Пока ничего интересного, но хозяин старается", reply_markup=kb.can_do)


@router_menu.callback_query(F.data == 'faq')
async def cmd_can_do(callback_query: CallbackQuery):
    await callback_query.answer('Частые вопросы')
    await callback_query.message.answer(f"Здесь будут ответы на часто задаваемые вопросы", reply_markup=kb.faq)


@router_menu.callback_query(F.data == 'travel_bel')
async def cmd_can_do(callback_query: CallbackQuery):
    await callback_query.answer('Командировки по РБ')
    await callback_query.message.answer(f"Здесь будет информация о командировках по РБ", reply_markup=kb_bel.inline_bel)
