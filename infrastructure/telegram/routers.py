from features.business_trips.handlers import router as router_trips
from features.main_menu.handlers import router as router_menu
from features.common.fallback_handlers import router as router_fallback
from features.advance_report.handlers import router as router_advance
from features.office_cat.handlers import router as router_cat

ALL_ROUTERS = [router_trips, router_menu, router_advance, router_cat, router_fallback]
