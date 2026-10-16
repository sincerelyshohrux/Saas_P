# SaaS Sales Platform

Django REST API (`backend/`) + React admin panel (`frontend/`).

## Ishga tushirish (birinchi marta)

### 1. DB va Redis
Docker bilan:   docker compose up -d db redis
Homebrew bilan: brew services start postgresql@16 redis

Postgres (Docker'siz) uchun bir marta:
    psql postgres -c "CREATE ROLE saas WITH LOGIN PASSWORD 'saas' CREATEDB;"
    psql postgres -c "CREATE DATABASE saas OWNER saas;"

### 2. Backend
    python3 -m venv venv && source venv/bin/activate
    pip install -r backend/requirements/dev.txt
    cd backend
    python manage.py migrate
    python manage.py createsuperuser
    pytest                        # 15 passed
    python manage.py runserver    # http://localhost:8000/api/docs/

### 3. Frontend (yangi terminal)
    cd frontend
    npm install
    npm run dev                   # http://localhost:5173

MUHIM: brauzerda http://localhost:5173 oching (127.0.0.1 emas, CORS faqat localhost uchun).

## Nima qayerda
| Nima | Fayl |
|---|---|
| Tenant izolyatsiyasi | backend/apps/core/mixins.py |
| Rollar va ruxsatlar | backend/apps/core/permissions.py |
| Dokon yaratish, parol berish | backend/apps/shops/views.py |
| Login, parol almashtirish | backend/apps/accounts/views.py |
| API klient + token refresh | frontend/src/shared/api/client.ts |
| Auth holati | frontend/src/features/auth/store.ts |
| Route himoyasi | frontend/src/app/guards.tsx |
| Sidebar layoutlar | frontend/src/layouts/ |
