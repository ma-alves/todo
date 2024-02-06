from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from todo.main import app
from todo.models import Base

import pytest


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:') # cria o banco na memória
    Session = sessionmaker(bind=engine) # cria uma fábrica de sessões
    Base.metadata.create_all(engine) # cria as tabelas do bd de teste
    yield Session() # fornece uma instância de Session que será injetada em cada teste que solicita a fixture session
    Base.metadata.drop_all(engine) # após cada teste que usa a fixture session, o banco é deletado
