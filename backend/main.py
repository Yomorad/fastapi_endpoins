from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel
import aioredis

app = FastAPI()
# для контейнера
redis = aioredis.from_url("redis://redis:6379")

# Модель данных: Создаем модель Data с полями phone и address с помощью Pydantic для валидации.
class Data(BaseModel):
    phone: str
    address: str

@app.post("/write_data")
async def write_data(data: Data):
    """
    Записывает данные в Redis по ключу phone.

    ## Параметры
    - **data**: Данные для записи в Redis.

    ## Пример запроса
    ```json
    {
        "phone": "89161234567",
        "address": "123 Main St"
    }
    ```

    ## Пример ответа
    ```json
    {
        "message": "Data saved successfully"
    }
    ```
    """
    await redis.set(data.phone, data.address)
    return {"message": "Data saved successfully"}

@app.get("/check_data")
async def check_data(phone: str):
    """
    Получает данные из Redis по ключу phone.

    ## Параметры
    - **phone**: Номер телефона для поиска в Redis.

    ## Пример запроса
    ```
    /check_data?phone=89161234567
    ```

    ## Пример ответа
    ```json
    {
        "phone": "89161234567",
        "address": "123 Main St"
    }
    ```
    """
    address = await redis.get(phone)
    return {"phone": phone, "address": address.decode("utf-8")}

openapi_schema = get_openapi(
    title="fastapi-redis_test API",
    version="1.0.0",
    routes=app.routes
)

app.openapi_schema = openapi_schema