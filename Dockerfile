FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

WORKDIR /app

# Copy requirements.txt ke dalam container
COPY ./app/requirements.txt /app/requirements.txt

# Install dependensi
RUN pip install -r requirements.txt

# Copy folder app (kode proyek)
COPY ./app /app
