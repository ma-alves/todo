from fastapi import FastAPI

from .schemas import Message
from .routes import auth, todos, users

app = FastAPI()


app.include_router(users.router)
app.include_router(auth.router)
app.include_router(todos.router)


@app.get('/', status_code=200, response_model=Message)
def home():
    return {'message': 'Oiee'}
