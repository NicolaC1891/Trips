from features.business_trips.flows.flow_trips_abroad import FLOW_TRIPS_ABROAD
from features.business_trips.flows.flow_trips_home import FLOW_TRIPS_HOME
from common.logger.logger import logger


class FlowResolver:
    def __init__(self):
        self.flows = {"home": FLOW_TRIPS_HOME, "abroad": FLOW_TRIPS_ABROAD}

    def __getitem__(self, prefix: str):
        try:
            return self.flows[prefix]
        except KeyError as e:
            logger.error("FlowResolver: failed to recognize key")
            raise KeyError(f"Invalid step key: {e}")
