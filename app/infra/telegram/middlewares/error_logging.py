from typing import Any, Callable

import sentry_sdk
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram.exceptions import TelegramAPIError

from app.infra.logs.logger import logger


class ErrorLoggingMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable, event: TelegramObject, data: dict[str, Any]) -> Any:
        try:
            return await handler(event, data)

        except TelegramAPIError as e:
            logger.warning(f"Telegram API Error: {e}")
            sentry_sdk.capture_exception(e)
            return

        except Exception as e:
            handler_name = getattr(handler, '__name__', repr(handler))
            logger.exception(f"Error in handler {handler_name} | event type: {type(event)} | error: {e}")
            sentry_sdk.capture_exception(e)
            return
