from sqlalchemy import select
from sqlalchemy.orm import Session

from todo.models import Todo, User


def test_create_user(session: Session):
    new_user = User(
        username='matheus',
        password='senha',
        email='matheusvialves@outlook.com',
    )
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'matheus'))

    assert user.username == 'matheus'


def test_create_todo(session: Session, user: User):
    todo = Todo(
        title='Test Todo',
        description='Test Desc',
        state='draft',
        user_id=user.id,
    )
    session.add(todo)
    session.commit()
    session.refresh(todo)

    user = session.scalar(select(User).where(User.id == user.id))

    assert todo in user.todos
