from abc import ABC, abstractmethod


class IFlowRepo(ABC):
    @abstractmethod
    async def get_response(self, table_name, step_key):
        pass
