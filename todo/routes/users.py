from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from todo.database import get_session
from todo.models import User
from todo.schemas import Message, UserList, UserPublic, UserSchema
from todo.security import (
    get_current_user,
    get_password_hash,
)


router = APIRouter(prefix='/users', tags=['users'])

# Annotated usado na aula 07, atribui a variável e seu tipo ao argumento
Session_ = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get('/', response_model=UserList)
def read_users(session: Session_, skip: int = 0, limit: int = 100):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()
    return {'users': users}


@router.get('/{user_id}', response_model=UserPublic)
def read_user(user_id: int, session: Session_):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(404, detail='Usuário não encontrado.')

    return db_user


@router.post('/', response_model=UserPublic, status_code=201)
def create_user(user: UserSchema, session: Session_):
    db_user = session.scalar(
        select(User).where(User.username == user.username)
    )
    if db_user:   # Mudar para email
        raise HTTPException(status_code=400, detail='Usuário já existe')

    hashed_password = get_password_hash(user.password)

    db_user = User(
        username=user.username, password=hashed_password, email=user.email
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.put('/{user_id}', response_model=UserPublic)
def update_user(
    current_user: CurrentUser,
    user_id: int,
    user: UserSchema,
    session: Session_,
):

    if current_user.id != user_id:
        raise HTTPException(status_code=400, detail='Not enough permissions')

    current_user.username = user.username
    current_user.password = get_password_hash(user.password)
    current_user.email = user.email
    session.commit()
    session.refresh(current_user)

    return current_user


@router.delete('/{user_id}', response_model=Message)
def delete_user(
    user_id: int,
    session: Session_,
    current_user: CurrentUser,
):

    if current_user.id != user_id:
        raise HTTPException(status_code=400, detail='Not enough permissions')

    session.delete(current_user)
    session.commit()

    return {'message': 'Usuário deletado.'}
