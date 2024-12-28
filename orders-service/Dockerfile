# Базовый лeгкий образ Python
FROM python:3.9-slim

# Установка нужных пакетов внутри контейнера
RUN pip install --upgrade pip
RUN pip install kafka-python sqlalchemy psycopg2-binary

WORKDIR /app
COPY app.py /app

# Запуск приложения
CMD ["python", "app.py"]
