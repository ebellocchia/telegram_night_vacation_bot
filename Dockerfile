# Build stage
FROM python:3.13-slim AS builder

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build

COPY pyproject.toml requirements.txt ./

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --prefix=/install -r requirements.txt

# Final stage
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY --from=builder /install /usr/local

WORKDIR /code
COPY bot_start.py .
COPY data/ data/
COPY telegram_night_vacation_bot/ telegram_night_vacation_bot/

CMD ["python", "bot_start.py"]
