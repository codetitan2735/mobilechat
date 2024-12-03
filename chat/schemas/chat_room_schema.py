from pydantic import validator
from pydantic.main import BaseModel
from pydantic.schema import UUID


class ChatRoomBaseSchema(BaseModel):

    name: str

    class Config:
        orm_mode = True


class CreateChatRoomSchema(ChatRoomBaseSchema):

    creator: UUID
    members: list[UUID]

    @validator('creator')
    def creator_to_str(cls, v):
        return str(v)

    @validator('members')
    def members_to_str(cls, v):
        return [str(member)for member in v]


class DetailChatRoomSchema(ChatRoomBaseSchema):

    id: UUID
    creator: UUID
    members: list[UUID]


class ListChatRoomSchema(BaseModel):

    __root__: list[DetailChatRoomSchema]

    class Config:
        orm_mode = True


class UpdateChatRoomNameSchema(ChatRoomBaseSchema):

    pass


class UpdateChatRoomMembersSchema(BaseModel):

    members: list[UUID]

    @validator('members')
    def members_to_str(cls, v):
        return [str(member)for member in v]