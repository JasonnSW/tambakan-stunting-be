FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

WORKDIR /app

COPY ./app /app

COPY .env /app/.env

RUN pip install -r requirements.txt

RUN chmod 600 /app/.env
