# Teste somente para fim didático
from jose import jwt

from todo.security import create_access_token
from todo.settings import Settings


def test_jwt():
    data = {'test': 'test'}
    token = create_access_token(data)
    settings = Settings()

    decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

    assert decoded['test'] == data['test']
    assert decoded['exp'] # Testa se o valor de exp foi adicionado
