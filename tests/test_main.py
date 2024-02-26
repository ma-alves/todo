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


def test_create_user_already_exists(client):
    response = client.post(
        '/users/',
        json={
            'username': 'matheus',
            'email': 'matheusvialves@outlook.com',
            'password': 'secret',
        }
    )
    response_again = client.post(
        '/users/',
        json={
            'username': 'matheus',
            'email': 'outro@outlook.com',
            'password': 'secret',
        }
    )
    print(response_again.json())
    assert response_again.status_code == 400
    assert response_again.json() == {
        'detail': 'Usuário já existe'
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


def test_update_user_not_found(client, user):
    response = client.put(
        '/users/404',
        json={
            'username': 'outro',
            'email': 'outro@outlook.com',
            'password': 'outro'
        },
    )
    assert response.status_code == 404
    assert response.json() == {'detail': 'Usuário não encontrado!'}


def test_delete_user(client, user):
    response = client.delete('/users/1')
    assert response.status_code == 200
    assert response.json() == {'message': 'Usuário deletado.'}


def test_delete_user_not_found(client, user):
    response = client.delete('/users/404')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Usuário não encontrado!'}


def test_read_one_user(client, user):
    response = client.get('/users/1')
    assert response.status_code == 200
    assert response.json() == {
        'username': 'Teste',
        'email': 'test@test.com',
    }
