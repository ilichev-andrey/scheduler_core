FROM python:3.9.2

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt ./

RUN apt-get update && \
    apt-get install -y libpq-dev && \
    pip install -U pip && pip install --no-cache-dir -r requirements.txt

COPY . .