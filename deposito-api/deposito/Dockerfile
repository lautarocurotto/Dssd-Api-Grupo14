# Dockerfile

FROM python:3.11-slim

# Instala las dependencias del sistema necesarias para psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev gcc

WORKDIR /app

COPY requirements.txt .

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Exponer el puerto
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
