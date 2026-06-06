# TeamFinder

Веб-приложение для поиска команды и проектов. Пользователи могут создавать проекты, находить участников, добавлять проекты в избранное и фильтровать участников по различным критериям.

## Стек технологий

- **Python** 3.12
- **Django** 5.2
- **PostgreSQL** 16
- HTML-шаблоны, CSS, JavaScript

## Запуск через Docker

1. Установите [Docker Desktop](https://www.docker.com/products/docker-desktop/).
2. В корне проекта скопируйте переменные окружения:
   ```bash
   cp .env_example .env
   ```
3. Запустите контейнеры:
   ```bash
   docker compose up --build
   ```
4. Откройте в браузере: http://localhost:8000

При первом запуске выполняются миграции, сбор статики и загрузка демо-данных.

### Тестовые пользователи (пароль у всех: `demo12345`)

| Email | Имя |
|-------|-----|
| anna@example.com | Анна Иванова |
| boris@example.com | Борис Петров |
| maria@example.com | Мария Сидорова |

Админ-панель: http://localhost:8000/admin/ (создайте суперпользователя командой ниже, если нужно).

Данные PostgreSQL и загруженные медиафайлы сохраняются в Docker volumes (`postgres_data`, `media_data`).

---

## Локальный запуск без Docker (только БД в Docker)

1. Создайте виртуальное окружение и установите зависимости:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. Скопируйте `.env_example` в `.env`:
   ```bash
   cp .env_example .env
   ```
3. Запустите только базу:
   ```bash
   docker compose up -d db
   ```
4. Примените миграции и демо-данные:
   ```bash
   python manage.py migrate
   python manage.py load_demo_data
   ```
5. Запустите сервер:
   ```bash
   python manage.py runserver
   ```

Сайт: http://localhost:8000

---

## Основные URL

- `/projects/list/` — список проектов
- `/projects/favorites/` — избранное (только для авторизованных)
- `/users/list/` — участники с фильтрами
- `/users/register/`, `/users/login/` — регистрация и вход

## Автор

**Измайлович Данил**
- GitHub: [reses1f](https://github.com/reses1f)
- Email: reses1f@vk.com
# team-finder
