from enum import Enum

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class TodoState(str, Enum):
    draft = 'draft'
    todo = 'todo'
    doing = 'doing'
    done = 'done'
    trash = 'trash'


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]

    todos: Mapped[list['Todo']] = relationship(
        back_populates='user', cascade='all, delete-orphan'
    )


class Todo(Base):
    __tablename__ = 'todos'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    state: Mapped[TodoState]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    user: Mapped[User] = relationship(back_populates='todos')


'''Neste ponto, é importante compreender o conceito de relationship em SQLAlchemy. 
A função relationship define como as duas tabelas irão interagir. 
O argumento back_populates permite uma associação bidirecional entre as tabelas, 
ou seja, se tivermos um usuário, podemos acessar suas tarefas através do atributo 
'todos', e se tivermos uma tarefa, podemos encontrar o usuário a que ela pertence 
através do atributo 'user'. O argumento cascade determina o que ocorre com as 
tarefas quando o usuário associado a elas é deletado. Ao definir 'all, delete-orphan',
 estamos instruindo o SQLAlchemy a deletar todas as tarefas de um usuário quando este 
 for deletado.
 '''