FROM python:3.11-slim


WORKDIR /backend

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

RUN pip install --upgrade pip

COPY ../.env ../

COPY backend/requirements.txt ./

RUN pip install -r requirements.txt \
    && useradd -U lctec \
    && install -d -m 0755 -o lctec -g lctec /backend/static

USER lctec:lctec
COPY --chown=lctec:lctec . .

COPY . ./