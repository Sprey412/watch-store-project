# Watch Store Project

## О проекте

Watch Store Project — это микросервисное приложение, демонстрирующее использование Docker, Kafka и PostgreSQL. Проект состоит из двух основных сервисов:

- **Catalog Service**: Управляет каталогом часов, позволяя добавлять новые товары.
- **Orders Service**: Обрабатывает заказы, полученные из Kafka, и сохраняет их в базе данных PostgreSQL.

## Технологии

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Apache Kafka](https://kafka.apache.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [Python 3.9](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Pytest](https://docs.pytest.org/)
- [Postman](https://www.postman.com/)

### Предварительные требования

- [Docker](https://www.docker.com/get-started) установлен на вашем компьютере.
- [Docker Compose](https://docs.docker.com/compose/install/) установлен.

### Установка

1. **Клонируйте репозиторий**:

    ```bash
    git clone https://github.com/Sprey412/watch-store-project.git
    cd watch-store-project
    ```

2. **Убедитесь, что необходимые порты свободны**:

    - PostgreSQL: `5432`
    - Catalog Service: `5000`
    - Kafka: `9092`
    - Zookeeper: `2181`

### Запуск приложения

1. **Соберите и запустите сервисы**:

    ```bash
    docker-compose up --build
    ```

    Эта команда создаст и запустит контейнеры для следующих сервисов:

    - **Zookeeper**: Необходим для работы Kafka.
    - **Kafka**: Брокер сообщений.
    - **PostgreSQL (`db`)**: База данных для хранения данных.
    - **Catalog Service**: Сервис для управления каталогом часов.
    - **Orders Service**: Сервис для обработки заказов.

2. **Проверьте состояние сервисов**:

    Вы можете проверить статус сервисов с помощью команды:

    ```bash
    docker-compose ps
    ```

    Все сервисы должны находиться в состоянии `Up` и иметь статус `healthy`.

## Использование API

### Добавление нового товара

Вы можете использовать [Postman](https://www.postman.com/) или `curl` для отправки POST-запросов в Catalog Service.

**Эндпоинт**: `POST http://localhost:5000/new-watch`

**Заголовки**:
- `Content-Type`: `application/json`

**Тело запроса**:

```json
{
  "watchName": "Rolex Submariner",
  "price": 10000
}