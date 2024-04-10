from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from todo.models import Base
from todo.settings import Settings


engine = create_engine(Settings().DATABASE_URL)
Base.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
