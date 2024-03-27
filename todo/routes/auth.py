from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from todo.database import get_session
from todo.models import User
from todo.schemas import Token
from todo.security import (
    create_access_token,
    get_current_user,
    verify_password,
)

router = APIRouter(prefix='/auth', tags=['auth'])

OAuth2Password = Annotated[OAuth2PasswordRequestForm, Depends()]
Session_ = Annotated[Session, Depends(get_session)]


@router.post('/token', response_model=Token)
def login_for_access_token(
    form_data: OAuth2Password,
    session: Session_,
):
    user = session.scalar(select(User).where(User.email == form_data.username))

    if not user:
        raise HTTPException(400, detail='Incorrect email or password.')

    if not verify_password(form_data.password, user.password):
        raise HTTPException(400, detail='Incorrect email or password.')

    access_token = create_access_token(data={'sub': user.email})

    return {'access_token': access_token, 'token_type': 'bearer'}


@router.post('/refresh_token', response_model=Token)
def refresh_access_token(
    user: User = Depends(get_current_user)
):
    new_access_token = create_access_token(data={'sub': user.email})

    return {'access_token': new_access_token, 'token_type': 'bearer'}
