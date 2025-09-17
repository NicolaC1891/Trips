from pydantic import BaseModel


class OfficeCatRequestDTO(BaseModel):
    response_key: str


class OfficeCatReplyDTO(BaseModel):
    reply: str
