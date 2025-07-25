from sqlalchemy import select

from app.application.interfaces.menu_item_i import MenuItemRepoInterface
from app.infra.rel_db.SQLA import MenuItem


class MenuItemRepo(MenuItemRepoInterface):

    def __init__(self, session):
        self.session = session

    async def get_response(self, response_key) -> str:
        statement = select(MenuItem).where(MenuItem.key == response_key)
        result = await self.session.execute(statement)
        row = result.scalar_one_or_none()
        return row.response if row else None
