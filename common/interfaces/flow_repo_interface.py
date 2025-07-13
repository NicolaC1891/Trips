from abc import ABC, abstractmethod


class FlowRepoInterface(ABC):    # abstract base class - as template for different implementations
    @abstractmethod    # child classes must implement all such methods
    async def get_response(self, response_key: str) -> str:
        pass
