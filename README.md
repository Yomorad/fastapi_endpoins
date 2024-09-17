<p>Первое задание</p>

сделано:
асинхронный редис
документация к эндпоинтам
использует пайдантик для создания схемы
валидация номера телефона в любом виде
обработчики ошибок
используется Depends
используется dotenv

в плане:
архитектура
используется Depends

```bash
    http://0.0.0.0:8000
    http://0.0.0.0:8000/docs    дока swagger
```
<p>Запросы:</p>

```bash
    post: http://0.0.0.0:8000/write_data 
        {
        "phone": "8916123456713",
        "address": "123 Main St, City"
        }
    get: http://localhost:8000/check_data?phone=8916123456713
    post: http://0.0.0.0:8000/update_data
        {
        "phone": "8916123456713",
        "address": "321 Main St, City"
        }
```

<p>Второе задание (Решение)</p>

```bash
UPDATE full_names f
SET status = s.status
FROM short_names s
WHERE SUBSTRING(f.name FROM 1 FOR POSITION('.' IN f.name) - 1) = s.name;
```
<p> Пояснение: сопоставяем данные двух таблиц по условию, перед этим обрезаем расширение по точке с помощью SUBSTRING</p>
<p> в случае если расширение отсутствует, добавим условие POSITION('.' IN s.name) > 0</p>

```bash
UPDATE full_names f
SET status = s.status
FROM short_names s
WHERE POSITION('.' IN f.name) > 0
  AND SUBSTRING(f.name FROM 1 FOR POSITION('.' IN f.name) - 1) = s.name;
```