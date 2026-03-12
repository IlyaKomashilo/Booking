# Booking API

FastAPI-сервис для управления отелями, категориями номеров, удобствами, пользователями и бронированиями.

## Требования

- Python 3.12+
- PostgreSQL

## Запуск

1. Установить зависимости:
   ```bash
   pip install -r requirements.txt
   ```
2. Создать `.env` с переменными:
   - `DB_NAME`, `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASS`
   - `JWT_SECRET_KEY`, `JWT_ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES`
3. Применить миграции:
   ```bash
   alembic upgrade head
   ```
4. Запустить приложение:
   ```bash
   uvicorn uvicorn src.main:app --reload
   ```

Документация OpenAPI доступна по адресу: `http://localhost:8000/docs`.
