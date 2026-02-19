FROM python:3.12-slim

WORKDIR /lms

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip poetry
RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-interaction --no-ansi --no-root

COPY . .

RUN mkdir -p /lms/media

EXPOSE 8000

CMD ["gunicorn", "crswrk_5.wsgi:application", "--bind", "0.0.0.0:8000"]