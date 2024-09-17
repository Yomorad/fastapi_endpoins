import re
from pydantic import BaseModel, Field, field_validator

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
