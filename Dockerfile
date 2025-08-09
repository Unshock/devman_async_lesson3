FROM python:3.10.0-slim-bullseye

ADD . /app
WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    zip \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
RUN pip install -r requirements.txt


CMD ["python", "server.py"]