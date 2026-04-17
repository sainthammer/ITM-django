# Django + PostgreSQL (Docker Compose)

Простой dev-setup для Django-проекта с PostgreSQL в отдельных контейнерах.

## Стек

- Python 3.13  
- Django 6  
- PostgreSQL 16  
- Docker / Docker Compose  

## Быстрый старт

### 1. Клонировать репозиторий

```bash
git clone <your-repo>
cd <your-repo>
```

### 2. Создать `.env`

```
SECRET_KEY=django-insecure-change-me
DEBUG=True

DB_NAME=mysite
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

### 3. Запуск проекта

```bash
docker compose up --build
```

Открыть в браузере:

http://localhost:8000/

## Создание суперпользователя

```bash
docker compose exec web python manage.py createsuperuser
```

Админка:

http://localhost:8000/admin/

## Основные команды

Остановить:
```bash
docker compose down
```

Сброс (удаляет БД):
```bash
docker compose down -v
```

Пересборка:
```bash
docker compose up --build
```

## Работа с БД

```bash
docker compose exec db psql -U postgres -d mysite
```

## Логи

```bash
docker compose logs -f web
```

Файл логов:
logs/app.log

## Медиа

http://localhost:8000/media/<filename>

## Проверка

```bash
docker compose ps
```

## Структура

```
.
├── compose.yaml
├── Dockerfile
├── .env
├── manage.py
├── requirements.txt
├── mysite/
├── images/
├── media/
├── logs/
└── docker/
```

## Важно

- HOST = db (не localhost)
- данные Postgres в volume
- .env обязателен
