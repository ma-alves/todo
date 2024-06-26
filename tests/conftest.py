from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from tests.factories import UserFactory
from todo.database import get_session
from todo.main import app
from todo.models import Base
from todo.security import get_password_hash
from todo.settings import Settings

import pytest


@pytest.fixture
def session():
    engine = create_engine(Settings().DATABASE_URL) 
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(engine)
    with Session() as session:
        yield session 
        session.rollback()
    
    Base.metadata.drop_all(engine) 


@pytest.fixture
def client(session: Session):
    def get_session_override():
        return session
    
    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def user(session: Session):
    password = 'testtest'
    user = UserFactory(password=get_password_hash(password))

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = 'testtest'

    return user


@pytest.fixture
def other_user(session: Session):
    password = 'testtest'
    user = UserFactory(password=get_password_hash(password))

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = 'testtest'

    return user


@pytest.fixture
def token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    return response.json()['access_token']
