from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from todo.database import get_session
from todo.main import app
from todo.models import Base, User

import pytest


@pytest.fixture
def client(session):
    def get_session_override():
        return session
    
    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread' : False},
        poolclass=StaticPool,
        ) # cria o banco na memória
    Base.metadata.create_all(engine) # cria as tabelas do bd de teste
    Session = sessionmaker(bind=engine) # cria uma fábrica de sessões
    yield Session() # fornece uma instância de Session que será injetada em cada teste que solicita a fixture session
    Base.metadata.drop_all(engine) # após cada teste que usa a fixture session, o banco é deletado


@pytest.fixture
def user(session):
    user = User(username='Teste', email='test@test.com', password='Testtest')
    session.add(user)
    session.commit()
    session.refresh(user)

    return user
