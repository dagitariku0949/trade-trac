#!/bin/bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
cd backend
exec gunicorn --bind 0.0.0.0:$PORT --workers 2 app:app
