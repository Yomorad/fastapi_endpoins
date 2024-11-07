Содержание задания указано в .jpg, в корне проекта
# RESTfull сервис FastAPI + Redis

## Сделано:
- асинхронный редис
- документация к эндпоинтам
- используется пайдантик для создания схемы
- валидация номера телефона
- обработчики ошибок
- используется dotenv
- архитектура - роутинг с валидацией отделил от приложения, вынес отдельно redis_client
- используется Depends для redis чтоб управлять подключением если что заменить на mock

## Как развернуть проект:
### 1 Клонируем проект

```bash
git clone https://github.com/Yomorad/fastapi-monitoring.git
```

### 2 Запуск Redis
```bash
# как вариант просто поднимаем ещё один контейнер
docker run --name redis-container -d -p 6379:6379 redis:latest
```
### 3 Запуск приложения

```bash
# из корня проекта:
# собираем образ
docker build -t myfastapiapp .
# поднимаем контейнер
docker run --name fastapi-container -d -p 8000:8000 myfastapiapp
```
## Тестируем запросы

```bash
# Uri приложения:
http://0.0.0.0:8000
http://0.0.0.0:8000/docs    дока swagger
# примеры запросов (Postman)
POST http://0.0.0.0:8000/write_data 
    {
    "phone": "8916123456713",
    "address": "123 Main St, City"
    }
GET http://localhost:8000/check_data?phone=8916123456713
POST http://0.0.0.0:8000/update_data
    {
    "phone": "8916123456713",
    "address": "321 Main St, City"
    }
```
# SQL-запросы

1. Сопоставяем данные двух таблиц по условию, перед этим обрезаем расширение по точке с помощью SUBSTRING</p>
```bash
UPDATE full_names f
SET status = s.status
FROM short_names s
WHERE SUBSTRING(f.name FROM 1 FOR POSITION('.' IN f.name) - 1) = s.name;
```
2. В случае если расширение отсутствует, добавим условие POSITION('.' IN s.name) > 0</p>

```bash
UPDATE full_names f
SET status = s.status
FROM short_names s
WHERE POSITION('.' IN f.name) > 0
  AND SUBSTRING(f.name FROM 1 FOR POSITION('.' IN f.name) - 1) = s.name;
```