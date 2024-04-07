#!/bin/sh

# Executa migrações do banco de dados
alembic upgrade head

# Inicia a aplicação
uvicorn todo.main:app --host 0.0.0.0 --port 8000
