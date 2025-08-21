# API для YaTube

REST API для социальной платформы YaTube. Обеспечивает управление постами, комментариями и подписками пользователей.

## Технологии
- Django 5.1.1
- Django REST Framework 3.15.2
- JWT аутентификация (djoser)
- SQLite

## Установка

```bash
git clone git@github.com:hawkxdev/api-final-yatube.git
cd api-final-yatube
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows
pip install -r requirements.txt
python yatube_api/manage.py migrate
python yatube_api/manage.py createsuperuser
python yatube_api/manage.py runserver
```

Документация: http://127.0.0.1:8000/redoc/

## API Endpoints

- `GET /api/v1/posts/` - список постов
- `POST /api/v1/posts/` - создать пост
- `GET/POST /api/v1/follow/` - подписки (только авторизованные)
- `GET /api/v1/groups/` - группы

## Аутентификация

```bash
# Получить JWT токен
curl -X POST http://127.0.0.1:8000/api/v1/auth/jwt/create/ \
     -H "Content-Type: application/json" \
     -d '{"username": "user", "password": "pass"}'

# Использовать токен
curl -H "Authorization: Bearer <access_token>" \
     http://127.0.0.1:8000/api/v1/posts/
```

## Права доступа

- **Анонимы**: только чтение (кроме /follow/)
- **Авторизованные**: создание и редактирование своего контента
- **Endpoint /follow/**: только для авторизованных (401 для анонимов)
