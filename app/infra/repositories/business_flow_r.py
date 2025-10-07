import json

from sqlalchemy import select
from app.application.interfaces.business_flow_i import IFlowRepo
from app.application.entities.flowstep import FlowStep
from app.infra.rel_db.SQLA import HomeFlow, AbroadFlow, RepexpFlow, MenuItem, AdvanceItem, PlannerFlow, TimesheetFlow

MODEL_MAP = {
    "home": HomeFlow,
    "abroad": AbroadFlow,
    "repexp": RepexpFlow,
    "menu": MenuItem,
    "advance": AdvanceItem,
    "planner": PlannerFlow,
    "timesheet": TimesheetFlow
}


class FlowRepo(IFlowRepo):

    def __init__(self, session):
        self.session = session

    async def get_response(self, table_name, step_key):
        print(table_name, step_key)
        table_model = MODEL_MAP.get(table_name)
        statement = select(table_model).where(table_model.key == step_key)
        result = await self.session.execute(statement)
        record = result.scalar_one_or_none()
        step = FlowStep(
            key=record.key,
            response=record.response,
            children=json.loads(record.children) if record.children != "0" else None,
            prev=record.prev if record.prev != "0" else None,
            next_=record.next_ if record.next_ != "0" else None,
            parent=record.parent if record.parent != "0" else None,
            label=record.label
        )
        return step
