from datetime import datetime

from bson import ObjectId
from pydantic import BaseModel, Field
from pydantic.schema import UUID


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class MessageModel(BaseModel):

    text: str = Field(...)
    timestamp: datetime = Field(...)
    author_id: UUID = Field(...)


class ChatRoomModel(BaseModel):

    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    origin_chat_room_id: str = Field(...)
    messages: list[MessageModel] = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
