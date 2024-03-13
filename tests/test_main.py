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


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
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


def test_update_user_has_no_perm(client, user, token):
    response = client.put(
        '/users/400',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'outro',
            'email': 'outro@outlook.com',
            'password': 'outro'
        },
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'Not enough permissions'}


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == 200
    assert response.json() == {'message': 'Usuário deletado.'}


def test_delete_user_has_no_perm(client, user, token):
    response = client.delete(
        '/users/404',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'Not enough permissions'}


def test_read_one_user(client, user):
    response = client.get('/users/1')
    assert response.status_code == 200
    assert response.json() == {
        'username': 'Teste',
        'email': 'test@test.com',
    }


def test_get_token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    token = response.json()

    assert response.status_code == 200
    assert 'access_token' in token
    assert 'token_type' in token
