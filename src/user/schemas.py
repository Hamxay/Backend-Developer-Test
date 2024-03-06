from pydantic import BaseModel, EmailStr


class User(BaseModel):
    """
    Schema representing user data for registration.
    """

    username: str
    email: EmailStr
    password: str


class ResponseUserSchema(BaseModel):
    """
    Schema representing the response after user registration or login.
    """

    token: str


class UserRelation(BaseModel):
    """
    Schema representing the relationship between users.
    """

    user_id: int


class UserLoginSchema(BaseModel):
    """
    Schema representing user login credentials.
    """

    email: EmailStr
    password: str


class TokenSchema(BaseModel):
    """
    Schema representing the JWT access token.
    """

    token: str
