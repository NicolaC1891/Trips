from aiogram import Dispatcher

from app.infra.logs.logger import logger
from app.infra.telegram.middlewares.logging import LoggingMiddleware
from app.ui.handlers.business_flow.router import router as router_flow
from app.ui.handlers.menu.router import router as router_menu
from app.ui.handlers.fallback import router as router_fallback
from app.ui.handlers.advance_report.handlers import router as router_advance
from app.ui.handlers.planner.planner_handlers import router as router_planner
from app.ui.handlers.calendar.handle_navigation import router as router_calendar

ALL_ROUTERS = [router_flow, router_menu, router_calendar, router_advance, router_planner, router_fallback]


async def startup():
    logger.info("Bot launched...")


async def shutdown():
    logger.info("Bot terminated...")


def create_dispatcher():
    dp = Dispatcher()
    dp.startup.register(startup)
    dp.shutdown.register(shutdown)
    dp.include_routers(*ALL_ROUTERS)
    dp.update.middleware(LoggingMiddleware())
    return dp
