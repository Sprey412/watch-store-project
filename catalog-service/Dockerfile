# Базовый лeгкий образ Python
FROM python:3.9-slim

# Установка нужных пакетов внутри контейнера
RUN pip install --upgrade pip
RUN pip install flask kafka-python sqlalchemy psycopg2-binary
# Flask (для веб-сервиса), kafka-python (для работы с Kafka), sqlalchemy (для работы с базой данных) и psycopg2-binary (для работы с PostgreSQL)

# Копирование кода внутрь контейнера
WORKDIR /app 
COPY app.py /app

# Запуск приложения
CMD ["python", "app.py"]
# При старте контейнера запустится Flask-приложение