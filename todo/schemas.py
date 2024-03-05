from pydantic import BaseModel, ConfigDict, EmailStr


class Message(BaseModel):
    message: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)
    # permite que o schema do pydantic seja convertido a partir de um modelo do sqlalchemy


class UserList(BaseModel):
    users: list[UserPublic]