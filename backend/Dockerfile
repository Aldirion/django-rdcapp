#syntax=docker/dockerfile:1
FROM python:3

WORKDIR /backend

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /backend/

