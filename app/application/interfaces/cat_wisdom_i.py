from abc import ABC, abstractmethod


class ICatWisdomRepo(ABC):
    @abstractmethod
    async def read_wisdom(self, wisdom_id: int) -> str:
        pass

    @abstractmethod
    async def read_all_ids(self) -> list[int]:
        pass
