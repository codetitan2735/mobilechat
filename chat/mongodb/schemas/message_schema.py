from datetime import datetime

from pydantic import BaseModel
from pydantic.schema import UUID


class MessageSchema(BaseModel):

    text: str
    timestamp: datetime
    author_id: UUID
