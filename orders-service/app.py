import time
import json
import os
from kafka import KafkaConsumer

# Считываем адрес Kafka из переменных окружения
bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092') # localhost:9092 - адрес по умолчанию

def main():
    # Создаём консюмера, подписанного на топик "new-watches"
    consumer = KafkaConsumer(
        'new-watches', # Название топика
        bootstrap_servers=bootstrap_servers, # Адрес Kafka
        group_id='orders-service-group',  # можно любое имя группы
        value_deserializer=lambda v: json.loads(v.decode('utf-8')), # Для десериализации JSON
        auto_offset_reset='earliest' # Считываем все сообщения с начала
    )

    print("Orders service is running. Waiting for new watches...") # Сообщение о запуске

    # Бесконечный цикл, слушаем новые сообщения
    for message in consumer: # Перебираем сообщения
        watch_info = message.value # Получаем данные из сообщения
        watch_name = watch_info.get('watchName') # Получаем название часов
        price = watch_info.get('price') # Получаем цену
        print(f"[orders-service] Получено новое сообщение: Часы '{watch_name}', цена {price}") # Выводим информацию в консоль
        # Здесь можно хранить логику: сохранить в базу, сформировать заказ и т.д.

if __name__ == '__main__': # Если файл запускается как основной
    # Даем Kafka время подняться
    time.sleep(5) # Ждем 5 секунд
    main() # Запускаем основную функцию
