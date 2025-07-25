from aiogram import Dispatcher

from app.infra.logs.logger import logger
from app.infra.telegram.middlewares.error_logging import ErrorLoggingMiddleware
from app.ui.handlers.business_flow.router import router as router_trips
from app.ui.handlers.menu.router import router as router_menu
from app.ui.handlers.fallback import router as router_fallback
from app.ui.handlers.advance_report.handlers import router as router_advance
from app.ui.handlers.office_cat.router import router as router_cat

ALL_ROUTERS = [router_trips, router_menu, router_advance, router_cat, router_fallback]


async def startup():
    logger.info("Bot launched...")


async def shutdown():
    logger.info("Bot terminated...")


def create_dispatcher():
    dp = Dispatcher()
    dp.startup.register(startup)
    dp.shutdown.register(shutdown)
    dp.include_routers(*ALL_ROUTERS)
    dp.update.middleware(ErrorLoggingMiddleware())
    return dp
