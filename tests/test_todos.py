from tests.factories import TodoFactory
from todo.models import Todo, TodoState, User


def test_create_todo(client, token):
    response = client.post(
        '/todos',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'Todo title test',
            'description': 'Todo description test',
            'state': 'draft',
        }
    )
    assert response.json() == {
        'id': 1,
        'title': 'Todo title test',
        'description': 'Todo description test',
        'state': 'draft',
    }
    

def test_list_todos(client, user, session, token):
    session.bulk_save_objects(TodoFactory.create_batch(5, user_id = user.id))
    session.commit()

    response = client.get(
        '/todos',
        headers={'Authorization': f'Bearer {token}'},
    )
    
    assert len(response.json()['todos']) == 5


def test_list_todos_pagination(client, user, session, token):
    session.bulk_save_objects(TodoFactory.create_batch(5, user_id = user.id))
    session.commit()

    response = client.get(
        '/todos/?offset=1&limit=2',
        headers={'Authorization': f'Bearer {token}'},
    )
    
    assert len(response.json()['todos']) == 2


def test_list_todos_title(client, user, session, token):
    session.bulk_save_objects(
        TodoFactory.create_batch(5, user_id = user.id, title='Test Todo 1')
    )
    session.commit()

    response = client.get(
        '/todos/?title=Test Todo 1',
        headers={'Authorization': f'Bearer {token}'},
    )
    
    assert len(response.json()['todos']) == 5


def test_list_todos_description(client, user, session, token):
    session.bulk_save_objects(
        TodoFactory.create_batch(5, user_id = user.id, description='description')
    )
    session.commit()

    response = client.get(
        '/todos/?description=desc', # 'desc' para reforçar que a Query é como 'LIKE'
        headers={'Authorization': f'Bearer {token}'},
    )
    
    assert len(response.json()['todos']) == 5


def test_list_todos_state(client, user, session, token):
    session.bulk_save_objects(
        TodoFactory.create_batch(5, user_id = user.id, state=TodoState.draft)  
    )
    session.commit()

    response = client.get(
        '/todos/?state=draft',
        headers={'Authorization': f'Bearer {token}'},
    )
    
    assert len(response.json()['todos']) == 5


def test_list_todos_combined(client, user, session, token):
    session.bulk_save_objects(
        TodoFactory.create_batch(
            5,
            user_id = user.id,
            title='Title Combined',
            description='Description Combined',
            state=TodoState.done,
        )
    )
    session.bulk_save_objects(
        TodoFactory.create_batch(
            3,
            user_id = user.id,
            title='Other Title Combined',
            description='Other Description Combined',
            state=TodoState.todo,
        )
    )
    session.commit()

    response = client.get(
        '/todos/?title=Title Combined&description=combined&state=done',
        headers={'Authorization': f'Bearer {token}'},
    )
    
    assert len(response.json()['todos']) == 5


def test_patch_todo_error(client, token):
    response = client.patch(
        '/todos/10',
        json={},
        headers={'Authorization': f'Bearer {token}'}  
    )
    assert response.status_code == 404
    assert response.json() == {'detail': 'Task not found.'}


def test_patch_todo(client, session, user, token):
    todo = TodoFactory(user_id=user.id)
    session.add(todo)
    session.commit()

    response = client.patch(
        f'/todos/{todo.id}',
        json={'title': 'teste!'},
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 200
    assert response.json()['title'] == 'teste!'


def test_delete_todo(client, session, user, token):
    todo = TodoFactory(user_id=user.id)
    session.add(todo)
    session.commit()

    response = client.delete(
        f'/todos/{todo.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 200
    assert response.json() == {
        'message': 'Task has been deleted successfully.'
    }


def test_delete_todo_error(client, token):
    response = client.delete(
        '/todos/10', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 404
    assert response.json() == {'detail': 'Task not found.'}
