from sqlalchemy import select

from app.application.interfaces.cat_wisdom_i import CatWisdomRepoInterface
from app.infra.rel_db.SQLA import CatWisdom


class CatWisdomRepo(CatWisdomRepoInterface):

    def __init__(self, session):
        self.session = session

    async def read_wisdom(self, wisdom_id: int) -> str:
        statement = select(CatWisdom).where(CatWisdom.id == wisdom_id)
        result = await self.session.execute(statement)
        response = result.scalar_one_or_none()
        return response.wisdom

    async def read_all_ids(self) -> list[int]:
        query = select(CatWisdom.id)
        result = await self.session.execute(query)
        ids = result.scalars().all()
        return ids
