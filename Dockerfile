FROM python:3.9-buster

COPY . /app
WORKDIR /app
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install netcat-openbsd

RUN pip install -r requirements.txt
