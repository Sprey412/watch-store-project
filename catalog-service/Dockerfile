# Базовый лeгкий образ Python
FROM python:3.9-slim

# Установка нужных пакетов
RUN pip install flask kafka-python 
# Flask (для веб-сервиса) и kafka-python (для работы с Kafka)

# Копирование кода внутрь контейнера
WORKDIR /app 
COPY app.py /app

# Запуск приложения
CMD ["python", "app.py"]
# При старте контейнера запустится Flask-приложение