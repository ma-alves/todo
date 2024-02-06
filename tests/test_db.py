from sqlalchemy import select

from todo.models import User


def test_create_user(session):
    new_user = User(
        username='matheus',
        password='senha',
        email='matheusvialves@outlook.com',
    )
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'matheus'))

    assert user.username == 'matheus'
