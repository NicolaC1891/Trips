from abc import ABC, abstractmethod


class CatWisdomRepoInterface(ABC):  # Use Protocol when refactor
    @abstractmethod  # child classes must implement all such methods
    async def read_wisdom(self, wisdom_id: str) -> str:
        pass

    @abstractmethod
    async def read_all_ids(self) -> list[int]:
        pass
