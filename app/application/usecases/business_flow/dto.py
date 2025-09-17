from pydantic import BaseModel

class FlowStepRequestDTO(BaseModel):
    flow_prefix: str
    step_key: str


class FlowStepReplyDTO(BaseModel):
    key: str | None
    response: str | None
    children: list | None
    prev: str | None
    next_: str | None
    parent: str | None
    label: str | None

    class Config:
        arbitrary_types_allowed = True
