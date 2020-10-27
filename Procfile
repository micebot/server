web: alembic upgrade head && gunicorn -k uvicorn.workers.UvicornWorker --bind "0.0.0.0:${PORT:-5000}" server:app --timeout 120
