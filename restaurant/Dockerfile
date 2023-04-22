FROM python:3.9-slim
ENV PYTHONBUFFERED=1

WORKDIR /app
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .

# CMD ["django", "run", "--host", "0.0.0.0", "--port", "8000"]