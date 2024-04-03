from todo.models import TodoState

from pydantic import BaseModel, ConfigDict, EmailStr


class Message(BaseModel):
    message: str


# Valida dados de entrada
class TodoSchema(BaseModel):
    title: str
    description: str
    state: TodoState


# Valida dados de saída
class TodoPublic(BaseModel):
    id: int
    title: str
    description: str
    state: TodoState


class TodoList(BaseModel):
    todos: list[TodoPublic]


# Atributos são opcionais pois nem todos são atualizados - PATCH method
class TodoUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    state: str | None = None


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
