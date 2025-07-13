from features.business_trips.flows.flow_trips_abroad import FLOW_TRIPS_ABROAD
from features.business_trips.flows.flow_trips_home import FLOW_TRIPS_HOME


class FlowResolver:
    def __init__(self):
        self.flows = {"home": FLOW_TRIPS_HOME, "abroad": FLOW_TRIPS_ABROAD}

    def __getitem__(self, prefix: str):
        return self.flows[prefix]