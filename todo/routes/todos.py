from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from todo.database import get_session
from todo.models import Todo, User
from todo.schemas import Message, TodoList, TodoPublic, TodoSchema, TodoUpdate
from todo.security import get_current_user

router = APIRouter(prefix='/todos', tags=['todos'])

CurrentUser = Annotated[User, Depends(get_current_user)]
Session_ = Annotated[Session, Depends(get_session)]

# 422 status_code: checar arg com schema do pydantic 

@router.post('/', response_model=TodoPublic)
def create_todo(
    todo: TodoSchema,
    user: CurrentUser,
    session: Session_,
):
    db_todo: Todo = Todo(
        title=todo.title,
        description=todo.description,
        state=todo.state,
        user_id=user.id
    )
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo


@router.get('/', response_model=TodoList)
def list_todos(
    session: Session_,
    user: CurrentUser,
    title: str = Query(None),
    description: str = Query(None),
    state: str = Query(None),
    offset: int = Query(None),
    limit: int = Query(None),
):
    query = select(Todo).where(Todo.user_id == user.id)

    if title:
        query = query.filter(Todo.title.contains(title))

    if description:
        query = query.filter(Todo.description.contains(description))

    if state:
        query = query.filter(Todo.state == state)

    todos = session.scalars(query.offset(offset).limit(limit)).all()

    return {'todos': todos}


@router.patch('/{todo_id}', response_model=TodoPublic)
def patch_todo(
    todo_id: int, todo: TodoUpdate, user: CurrentUser, session: Session_,
):
    db_todo = session.scalar(
        select(Todo).where(Todo.user_id == user.id, Todo.id == todo_id)
    )

    if not db_todo:
        raise HTTPException(404, detail='Task not found.')
    
    # Loop que pega os dados da requisição e 'seta' somente os que devem
    # ser alterados no objeto de resposta
    for key,value in todo.model_dump(exclude_unset=True).items():
        setattr(db_todo, key, value)

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo


@router.delete('/{todo_id}', response_model=Message)
def delete_todo(todo_id: int, session: Session_, user: CurrentUser):
    todo = session.scalar(
        select(Todo).where(Todo.id == todo_id, Todo.user_id == user.id)
    )

    if not todo:
        raise HTTPException(404, detail='Task not found.')
    
    session.delete(todo)
    session.commit()

    return {'message': 'Task has been deleted successfully.'}
