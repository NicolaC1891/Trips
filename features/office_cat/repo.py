from sqlalchemy import select

from features.office_cat.interfaces import CatWisdomRepoInterface
from infrastructure.database.ORMmodels import CatWisdom


class CatWisdomRepo(CatWisdomRepoInterface):

    def __init__(self, session):
        self.session = session

    async def read_wisdom(self, wisdom_id: str) -> str:
        statement = select(CatWisdom).where(CatWisdom.id == wisdom_id)
        result = await self.session.execute(statement)
        wisdom = result.scalar_one_or_none()
        return wisdom.phrase

    async def read_all_ids(self) -> list[int]:
        query = select(CatWisdom.id)
        result = await self.session.execute(query)
        ids = result.scalars().all()
        return ids
