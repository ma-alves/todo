from fastapi import FastAPI

from .schemas import UserPublic, UserSchema


app = FastAPI()


@app.get('/')
def home():
    return {'message': 'Oiee'}


@app.post('/users/', status_code=201, response_model=UserPublic)
def create_user(user: UserSchema):
    return user
