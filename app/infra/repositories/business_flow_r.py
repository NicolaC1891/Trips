import json

from sqlalchemy import select
from app.application.interfaces.business_flow_i import FlowRepoInterface
from app.application.usecases.business_flow.dto import FlowStepReplyDTO
from app.infra.rel_db.SQLA import HomeFlowStep, AbroadFlowStep, RepexpFlowStep, MenuItem, AdvanceItem

MODEL_MAP = {
    "home": HomeFlowStep,
    "abroad": AbroadFlowStep,
    "repexp": RepexpFlowStep,
    "menu": MenuItem,
    "advance": AdvanceItem
}

class FlowRepo(FlowRepoInterface):

    def __init__(self, session):
        self.session = session

    async def get_response(self, flow_name, response_key) -> FlowStepReplyDTO:
        table_name = MODEL_MAP.get(flow_name)
        statement = select(table_name).where(table_name.key == response_key)
        result = await self.session.execute(statement)
        record = result.scalar_one_or_none()
        response = FlowStepReplyDTO(
            key=record.key,
            response=record.response,
            children=json.loads(record.children) if record.children != "0" else None,
            prev=record.prev if record.prev != "0" else None,
            next_=record.next_ if record.next_ != "0" else None,
            parent=record.parent if record.parent != "0" else None,
            label=record.label
        )
        return response
