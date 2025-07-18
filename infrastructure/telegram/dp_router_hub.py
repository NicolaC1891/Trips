from aiogram import Dispatcher

from common.logger.logger import logger
from features.business_trips.handlers import router as router_trips
from features.main_menu.handlers import router as router_menu
from features.common.fallback_handlers import router as router_fallback
from features.advance_report.handlers import router as router_advance
from features.office_cat.handlers import router as router_cat

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
    return dp
