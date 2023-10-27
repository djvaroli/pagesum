FROM python:3.11-alpine

WORKDIR /workdir

COPY requirements.txt requirements.txt

COPY .env .env

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY /app ./app/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

