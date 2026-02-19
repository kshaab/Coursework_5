# Habit Tracker

### Проект трекера привычек (бэкенд-часть SPA веб-приложения), разработанный на **Django**.  

### Проект завершен.

## Содержание 

- [Использование](#использование)
- [Структура проекта](#структура-проекта)
- [Зависимости](#зависимости)
- [Celery](#celery-)
- [Технологии](#технологии)
- [Тестирование](#тестирование)
- [Deployment & CI/CD](#deployment--cicd)
- [GitHub Actions CI/CD](#github-actions-cicd)
- [Автор](#автор)


## Использование
Клонируйте репозиторий: 
```bash
git clone https://github.com/kshaab/Coursework_5
cd crswrk_5
```
Установите зависимости и активируйте виртуальное окружение: 
poetry install
poetry shell

Примените миграции: 
python manage.py migrate

Запустите сервер разработки: 
python manage.py runserver


## Структура проекта

### crswrk_5/
Основные настройки проекта и конфигурация Django. 

### habits/
Приложение для работы с привычками: модели, сериализаторы, вьюсеты, задачи Celery.

### users/
Приложение для работы с пользователями: регистрация, авторизация, профили, права доступа. 

## Зависимости
Управление зависимостями осуществляется через Poetry (pyproject.toml).
Основные зависимости:
- Django 5.x
- Celery 5.x
- PostgreSQL
- Redis (для Celery)

## Celery 
Проект использует Celery + Celery Beat для фоновых задач:
- Рассылка напоминаний о выполнении привычек в телеграм-бот. 


## Тестирование
Запуск тестов:
```bash
poetry run python manage.py test
```

Запуска теста отдельного приложения(пример): 
```bash
poetry run python manage.py test habits
```

## Deployment & CI/CD
1. Подключение к серверу по SSH
```bash
ssh user@SERVER_IP
```
2. Установка Docker и Docker Compose
```bash
sudo apt update
sudo apt install -y docker.io docker-compose-plugin
```
Проверка установки:
```bash
docker --version
docker compose version
```
3. Клонирование проекта
```bash
git clone https://github.com/kshaab/Coursework_5
cd crswrk_5
```
4. Создание .env
```bash
DEBUG=True
ALLOWED_HOSTS=*

POSTGRES_DB=habits_tracker
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=db
POSTGRES_PORT=5432

SECRET_KEY=your_secret_key
```
5. Запуск проекта
```bash
docker compose up -d --build
```
Проверка запуска: 
```bash
docker compose ps
```

Проверка приложения по адресу:
```cpp
http://158.160.94.191:8000
```
## GitHub Actions CI/CD
Workflow:
```bash
.github/workflows/
```

Workflow запускается автоматически при каждом push в репозиторий.

Этапы workflow:
1. Клонирование репозитория
2. Установка зависимостей
3. Запуск тестов (деплой выполняется только при успешном прохождении тестов.)
4. Подключение к серверу по SSH
5. Pull последних изменений
6. Пересборка контейнеров
7. Перезапуск приложения

## Технологии
- Python 3.13

- Django 5.x

- Django REST Framework 4.x

- PostgreSQL

- Redis 

- Celery 5.x

## Автор
[Ксения](https://github.com/kshaab)