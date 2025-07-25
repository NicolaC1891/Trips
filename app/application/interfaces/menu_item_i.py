from abc import ABC, abstractmethod


class MenuItemRepoInterface(ABC):

    @abstractmethod
    async def get_response(self, response_key) -> str:
        pass
