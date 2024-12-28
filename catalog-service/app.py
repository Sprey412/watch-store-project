from flask import Flask, request
from kafka import KafkaProducer
import json 
import os

app = Flask(__name__) # Создание Flask-приложение

# Чтение адреса Kafka из переменных окружения, которые указаны в docker-compose
bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')

# Создание продьюсера
producer = KafkaProducer(
    bootstrap_servers=bootstrap_servers, # Адрес Kafka
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Для отправки JSON
)

@app.route('/new-watch', methods=['POST']) # Декоратор для обработки POST-запросов на /new-watch
def new_watch(): # Функция для обработки запроса
    """
    Эндпоинт, который будет добавлять новые часы в каталог и отправлять сообщение в Kafka. 
    Пример тела запроса (JSON):
    {
      "watchName": "Casio Edifice",
      "price": 29990
    }
    """
    watch_data = request.json # Получаем JSON-тело запроса
    if not watch_data: # Если тело запроса пустое
        return {"error": "No JSON body provided"}, 400 # Возвращаем ошибку 400

    # Отправляем в Kafka топик "new-watches"
    producer.send('new-watches', watch_data) 
    producer.flush()  # принудительная отправка

    return {"message": f"New watch '{watch_data.get('watchName')}' was added"}, 200 # Возвращаем успешный ответ

@app.route('/') # Декоратор для обработки GET-запросов на /
def index(): # Функция для обработки запроса
    return "Catalog service is running! Use POST /new-watch to add a new watch." # Возвращаем простой текст

if __name__ == '__main__': # Если файл запускается как основной
    # Запуск Flask на 0.0.0.0, порт 5000
    app.run(host='0.0.0.0', port=5000, debug=True)
