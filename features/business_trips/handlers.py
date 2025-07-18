import sentry_sdk
from aiogram import Router
from aiogram.types import CallbackQuery

from common.logger.logger import logger
from features.business_trips.flows.flow_resolver import FlowResolver
from features.business_trips.usecases import FetchFlowStepUseCase
from infrastructure.database.session import async_session_factory
from domain.flow_logic import FlowStepValidator
from features.business_trips.flow_repo import FlowRepo
from features.business_trips.flow_kb_builder import FlowStepUIBuilder

router = Router()


@router.callback_query(lambda c: c.data.startswith(("home_", "abroad_")))
async def handler_trips(callback: CallbackQuery):
    await callback.answer()

    prefix = callback.data.split("_", 1)[0]
    step_key = callback.data

    try:
        async with async_session_factory() as session:
            flow = FlowResolver()[prefix]
            repo = FlowRepo(session)
            validator = FlowStepValidator()
            use_case = FetchFlowStepUseCase(
                flow=flow, step_key=step_key, validator=validator, repo=repo
            )
            step = await use_case.execute()
        reply = step.content
        keyboard = FlowStepUIBuilder(flow, step).build_kb()
        await callback.message.edit_text(text=reply, reply_markup=keyboard)

    except KeyError as e:
        logger.exception("Error: no step in flow")
        sentry_sdk.capture_exception(e)
        await callback.message.answer(
            "Ошибка! Напишите через «Идея!», что вы нажимали — и бот станет лучше!"
        )
        return

    except ValueError as e:
        logger.exception("Invalid flow step")
        sentry_sdk.capture_exception(e)
        await callback.message.answer(
            "Ошибка! Напишите через «Идея!», что вы нажимали — и бот станет лучше!"
        )
        return

    except Exception as e:
        logger.exception("Error in trips handler")
        sentry_sdk.capture_exception(e)
        await callback.message.answer("Произошла ошибка. Попробуйте позже.")
        return
