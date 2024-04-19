FROM python:3.11

RUN apt update \
    && apt install -y --no-install-recommends -y \
        build-essential

# Install Poetry

RUN mkdir /etc/poetry

ENV PATH="$PATH:/etc/poetry/bin"
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/etc/poetry python3 -

# Install dependencies globally
RUN poetry config virtualenvs.create false

RUN mkdir /app
WORKDIR /app

COPY ./pyproject.toml /app
COPY ./poetry.lock /app

RUN poetry install

CMD ["./deploy/local/django/run_django.sh"]
