from pydantic import BaseModel
from pydantic.schema import UUID


class RequestUserSchema(BaseModel):

    id: UUID
    username: str
