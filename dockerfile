
FROM python:3.12-slim


RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .


ENV DJANGO_SETTINGS_MODULE=base.settings
ENV PYTHONUNBUFFERED 1

# Запускаем команду для Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]