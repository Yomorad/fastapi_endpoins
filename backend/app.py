from fastapi import FastAPI, HTTPException, Response
from fastapi.openapi.utils import get_openapi
from routes.data_routes import router as data_router

app = FastAPI()

# Подключение маршрутов
app.include_router(data_router)

# Обработчик ошибок
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return Response(
        status_code=exc.status_code,
        content={"message": exc.detail}
    )

# Создание схемы OpenAPI
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="fastapi-redis_test API",
        version="1.0.0",
        routes=app.routes
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi