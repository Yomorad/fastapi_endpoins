FROM python:3.10
WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --upgrade pip --no-warn-script-location
RUN pip install -r requirements.txt --no-cache-dir --no-warn-script-location

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]