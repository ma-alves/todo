from fastapi.testclient import TestClient
from todo.main import app


def test_home_retorna_200_e_oiee(client):
    response = client.get('/')

    assert response.status_code == 200
    assert response.json() == {'message': 'Oiee'}
