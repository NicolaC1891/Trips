from sqlalchemy import select

from app.infra.rel_db.SQLA import FlowStepContent
from app.application.interfaces.business_flow_i import FlowRepoInterface


class FlowRepo(FlowRepoInterface):

    def __init__(self, session):
        self.session = session

    async def get_response(self, response_key) -> str:
        statement = select(FlowStepContent).where(FlowStepContent.key == response_key)
        result = await self.session.execute(statement)
        record = result.scalar_one_or_none()
        if record:
            return record.response
        else:
            return "Текст не найден"
