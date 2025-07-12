from sqlalchemy import select

from infrastructure.database.ORMmodels import FlowResponse
from common.interfaces.instruction import InstructionRepoInterface


class InstructionRepo(InstructionRepoInterface):

    def __init__(self, session):
        self.session = session

    async def get_response(self, response_key: str) -> str:
        statement = select(FlowResponse).filter_by(key=response_key)
        result = await self.session.execute(statement)
        row = result.scalar_one_or_none()
        if row:
            return row.response
        else:
            return "Текст инструкции не найден"
