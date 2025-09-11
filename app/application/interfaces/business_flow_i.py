from abc import ABC, abstractmethod


class FlowRepoInterface(
    ABC
):  # abstract base class - as template for different implementations
    @abstractmethod  # child classes must implement all such methods
    async def get_response(self, flow_name, response_key):
        pass
