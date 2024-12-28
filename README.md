# Watch Store Project

Пробный проект на Python + Kafka + Docker Compose.  
Состоит из двух микросервисов:
1. **catalog-service** (Producer) — отправляет сообщения в Kafka.
2. **orders-service** (Consumer) — читает сообщения из топика и обрабатывает их.

## Стек технологий
- Python 3.9
- Flask (для простого REST API)
- kafka-python
- Docker, Docker Compose
- Kafka (Confluent Platform образы)
- Zookeeper

## Как запустить
1. Клонировать репозиторий:
   ```bash
   git clone https://github.com/<USERNAME>/watch-store-project.git
   cd watch-store-project
