import os
import re
from fastapi import Depends, FastAPI, HTTPException, Response
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel, Field, field_validator
import aioredis
from dotenv import load_dotenv

app = FastAPI()

# подгружаем конфиги
load_dotenv()
redis = aioredis.from_url(os.getenv("REDIS_URL"))


# Модель данных: Создаем модель Data с полями phone и address с помощью Pydantic для валидации.
class Data(BaseModel):
    phone: str = Field(..., min_length=10, max_length=15, description="Phone number")
    address: str

    @field_validator('phone')
    def validate_phone(cls, value: str) -> str:
        pattern = r"^\+?\d{10,15}$"
        if not re.match(pattern, value):
            raise ValueError("Invalid phone number")
        return value
    
# Обработчик ошибок
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return Response(
        status_code=exc.status_code,
        content={"message": exc.detail}
    )

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
    try:
        await redis.set(data.phone, data.address)
        return {"message": "Данные успешно сохранены"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/update_data")
async def update_data(data: Data):
    """
    Обновление данных пользователя.

    Args:
        data (Data): Объект данных, содержащий номер телефона и адрес.
        username (str): Имя пользователя, выполнившего запрос.

    Returns:
        dict: Сообщение об успешном обновлении данных.

    Raises:
        HTTPException: Если возникает ошибка при обновлении данных.
    """
    try:
        # Проверка наличия ключа в Redis
        exists = await redis.exists(data.phone)
        if not exists:
            raise HTTPException(status_code=404, detail="Данные не найдены")

        await redis.set(data.phone, data.address)
        return {"message": "Данные успешно обновлены"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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
    try:
        address = await redis.get(phone)
        if address is None:
            raise HTTPException(status_code=404, detail="Данные не найдены")
        return {"phone": phone, "address": address.decode("utf-8")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

openapi_schema = get_openapi(
    title="fastapi-redis_test API",
    version="1.0.0",
    routes=app.routes
)

app.openapi_schema = openapi_schema