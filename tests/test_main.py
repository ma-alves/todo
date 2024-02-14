from fastapi.testclient import TestClient

from todo.main import app
from todo.schemas import UserPublic


def test_home_retorna_200_e_oiee(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'message': 'Oiee'}


def test_read_users(client):
    response = client.get('/users/')
    assert response.status_code == 200
    assert response.json() == {'users': []}


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'matheus',
            'email': 'matheusvialves@outlook.com',
            'password': 'secret',
        }
    )
    assert response.status_code == 201
    assert response.json() == {
        'username': 'matheus',
        'email': 'matheusvialves@outlook.com',
    }


def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user):
    response = client.put(
        '/users/1',
        json={
            'username': 'matheus',
            'email': 'matheusvialves@outlook.com',
            'password': 'newpassword'
        },
    )
    assert response.status_code == 200
    assert response.json() == {
            'username': 'matheus',
            'email': 'matheusvialves@outlook.com',
    }
