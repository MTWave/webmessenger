#!/bin/sh

export HOST=${HOST:-127.0.0.1}
export PORT=${PORT:-8081}

exec uvicorn --reload --host $HOST --port $PORT "osiris.main:app" --reload