from todo.schemas import UserPublic


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


def test_update_user_with_wrong_user(client, other_user, token):
    response = client.put(
        f'/users/{other_user.id}',
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


def test_delete_user_with_wrong_user(client, other_user, token):
    response = client.delete(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'Not enough permissions'}


def test_read_one_user(client, user):
    response = client.get(f'/users/{user.id}')
    assert response.status_code == 200
    assert response.json() == {
        'username': f'{user.username}',
        'email': f'{user.email}',
    }
