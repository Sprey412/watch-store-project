from flask import Flask, request, jsonify
from kafka import KafkaProducer
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker
import json
import os

app = Flask(__name__) # Создание Flask-приложение

# Конфигурация Kafka Producer
producer = KafkaProducer( # Создание продьюсера
    bootstrap_servers=os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092'), # Адрес Kafka
    value_serializer=lambda v: json.dumps(v).encode('utf-8') # Для отправки JSON
)

# Конфигурация базы данных
DATABASE_URL = os.getenv('DATABASE_URL')  # 'postgresql://watchuser:watchpass@db:5432/watchstore'
engine = create_engine(DATABASE_URL) # Создание подключения к базе данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # Создание сессии
Base = declarative_base() # Создание базового класса

# Модель для часов
class Watch(Base): # Создание модели
    __tablename__ = 'watches' # Название таблицы

    id = Column(Integer, primary_key=True, index=True) # Поле id
    name = Column(String, nullable=False) # Поле name
    price = Column(Float, nullable=False) # Поле price

# Создание таблиц
Base.metadata.create_all(bind=engine)

@app.route('/new-watch', methods=['POST']) # Обработчик POST-запроса
def add_watch(): # Функция добавления часов
    data = request.get_json() # Получение данных из запроса
    watch_name = data.get('watchName') # Получение названия часов
    price = data.get('price') # Получение цены

    if not watch_name or not price: # Если не переданы watchName или price
        return jsonify({"error": "watchName and price are required"}), 400 # Вернуть ошибку

    # Сохранение в базе данных
    session = SessionLocal() # Создание сессии
    new_watch = Watch(name=watch_name, price=price) # Создание новой записи
    session.add(new_watch) # Добавление записи
    session.commit() # Сохранение изменений
    session.refresh(new_watch) # Обновление записи
    session.close() # Закрытие сессии

    # Отправка сообщения в Kafka
    message = { # Создание сообщения
        "id": new_watch.id, # id новой записи
        "watchName": watch_name, # Название часов
        "price": price # Цена
    }
    producer.send('new-watches', value=message) # Отправка сообщения

    return jsonify({"message": f"New watch '{watch_name}' was added"}), 201 # Вернуть сообщение об успешном добавлении

if __name__ == '__main__': # Если файл запускается как основной
    app.run(host='0.0.0.0', port=5000) # Запуск приложения