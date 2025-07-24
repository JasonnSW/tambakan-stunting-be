FROM python:3.11-slim

WORKDIR /app

COPY ./app/requirements.txt /app/requirements.txt
RUN pip install six==1.16.0
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY ./app /app
COPY ./app/alembic /app/alembic
COPY ./app/alembic.ini /app/alembic.ini

CMD alembic upgrade head && gunicorn main:app -k uvicorn.workers.UvicornWorker -w 1 -b 0.0.0.0:8000 --timeout 120
