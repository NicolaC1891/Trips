from sqlalchemy import select

from infrastructure.database.ORMmodels import FlowResponse
from features.business_trips.flow_repo_interface import FlowRepoInterface


class FlowRepo(FlowRepoInterface):

    def __init__(self, session):
        self.session = session

    async def get_response(self, response_key: str) -> str:
        statement = select(FlowResponse).where(FlowResponse.key == response_key)
        result = await self.session.execute(statement)
        record = result.scalar_one_or_none()
        if record:
            return record.response
        else:
            return "Текст не найден"
