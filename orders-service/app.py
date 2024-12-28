from kafka import KafkaConsumer
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker
import json
import os

# Конфигурация базы данных
DATABASE_URL = os.getenv('DATABASE_URL')  # 'postgresql://watchuser:watchpass@db:5432/watchstore'
engine = create_engine(DATABASE_URL) # Создание подключения к базе данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # Создание сессии для работы с базой данных
Base = declarative_base() # Создание базового класса для моделей

# Модель для заказов
class Order(Base):
    __tablename__ = 'orders' # Название таблицы в базе данных

    id = Column(Integer, primary_key=True, index=True) # Поле id
    watch_id = Column(Integer, nullable=False) # Поле watch_id
    watch_name = Column(String, nullable=False) # Поле watch_name
    price = Column(Float, nullable=False) # Поле price

# Создание таблиц
Base.metadata.create_all(bind=engine)

# Основная функция
def main():
    consumer = KafkaConsumer( # Создание потребителя Kafka
        'new-watches', # Название топика
        bootstrap_servers=os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092'), # Сервер Kafka
        group_id='orders-service-group', # Группа потребителей
        value_deserializer=lambda m: json.loads(m.decode('utf-8')), # Десериализация данных
        auto_offset_reset='earliest' # Смещение
    )
    print("Orders service is running. Waiting for new watches...") # Вывод сообщения о запуске

    for message in consumer: # Цикл обработки сообщений
        data = message.value # Получение данных из сообщения
        watch_id = data.get('id') # Получение данных из сообщения
        watch_name = data.get('watchName') # Получение данных из сообщения
        price = data.get('price') # Получение данных из сообщения

        if watch_id and watch_name and price: # Проверка наличия данных
            # Сохранение в базе данных
            session = SessionLocal() # Создание сессии
            new_order = Order(watch_id=watch_id, watch_name=watch_name, price=price) # Создание нового заказа
            session.add(new_order) # Добавление заказа в сессию
            session.commit() # Сохранение изменений
            session.refresh(new_order) # Обновление заказа
            session.close() # Закрытие сессии

            print(f"Получено новое сообщение: Часы '{watch_name}', цена {price}") # Вывод сообщения
        else: # В случае некорректных данных
            print("Получено некорректное сообщение:", data)

if __name__ == '__main__': # Запуск основной функции
    main()