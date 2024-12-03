from pydantic import BaseModel, validator, EmailStr
from pydantic.types import UUID

from utils.hash_password import hash_string


class UserBaseSchema(BaseModel):

    username: str

    class Config:
        orm_mode = True


class UserRegisterSchema(UserBaseSchema):

    password: str
    email: EmailStr
    first_name: str
    last_name: str

    @validator('password')
    def password_hash(cls, v):
        return hash_string(v)


class UserLoginSchema(UserBaseSchema):

    password: str

    @validator('password')
    def password_hash(cls, v):
        return hash_string(v)


class UserRefreshTokensSchema(BaseModel):

    refresh_token: str


class UserRetrieveSchema(UserBaseSchema):

    id: UUID
    email: EmailStr
    first_name: str
    last_name: str


class UserListSchema(BaseModel):

    __root__: list[UserRetrieveSchema]

    class Config:
        orm_mode = True


class UserTokenPayloadSchema(UserBaseSchema):

    id: UUID

    @validator('id')
    def convert_id_to_str(cls, v):
        return str(v)


class SuccessLoginSchema(BaseModel):

    access_token: str
    refresh_token: str
