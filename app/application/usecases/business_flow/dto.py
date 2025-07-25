from pydantic import BaseModel

from app.application.entities.flow_step_entity import FlowStep


class FlowStepRequestDTO(BaseModel):
    flow_prefix: str
    step_key: str


class FlowStepReplyDTO(BaseModel):
    flow_step: FlowStep
    child_labels: list | None
    reply: str

    class Config:
        arbitrary_types_allowed = True
