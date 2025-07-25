from pydantic import BaseModel


class ShowMenuItemRequestDTO(BaseModel):
    response_key: str


class ShowMenuItemReplyDTO(BaseModel):
    reply: str
