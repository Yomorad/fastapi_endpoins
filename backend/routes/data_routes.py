from fastapi import APIRouter, Depends, HTTPException
from models.data import Data
from redis_client import get_redis, redis

router = APIRouter()

@router.post("/write_data")
async def write_data(data: Data, redis = Depends(get_redis)):
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

@router.post("/update_data")
async def update_data(data: Data, redis = Depends(get_redis)):
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

@router.get("/check_data")
async def check_data(phone: str, redis = Depends(get_redis)):
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