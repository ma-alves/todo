FROM python:3.12-slim

WORKDIR app/
COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000

CMD [ "uvicorn", "--host", "0.0.0.0", "todo.main:app" ]
