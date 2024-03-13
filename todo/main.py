from fastapi import FastAPI

from .schemas import Message
from .routes import auth, users

app = FastAPI()


app.include_router(users.router)
app.include_router(auth.router)


@app.get('/', status_code=200, response_model=Message)
def home():
    return {'message': 'Oiee'}
