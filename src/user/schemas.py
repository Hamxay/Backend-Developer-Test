from pydantic import BaseModel, EmailStr


class User(BaseModel):
    username: str
    email: EmailStr
    password: str


class ResponseUserSchema(BaseModel):
    token: str


class UserRelation(BaseModel):
    user_id: int


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str
