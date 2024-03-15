#syntax=docker/dockerfile:1
FROM python:3.10

WORKDIR /backend

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt ./
RUN pip3 install -r ./requirements.txt
# COPY . /backend/

# CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
# CMD ["make", "run"]

