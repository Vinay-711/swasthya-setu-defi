# SwasthyaSetu Deployment

## Local Docker Deployment

1. Copy environment template:

```bash
cp .env.example .env
cp backend/.env.example backend/.env
```

2. Start all services:

```bash
docker compose -f infrastructure/docker/docker-compose.yml up --build
```

3. Access apps:

- Frontend: http://localhost:3000
- Backend API docs: http://localhost:8000/docs
- pgAdmin: http://localhost:5050

5. Demo mode controls:

- Frontend default is mock mode (`VITE_DEFAULT_MOCK_MODE=true`).
- Every frontend request auto-appends `?mock=true` while mock mode is ON.
- Use the top bar toggle (`Mock: ON/OFF`) to switch between demo-safe mock and live mode instantly.

4. Apply migrations (optional when tables are already auto-created):

```bash
cd backend
alembic upgrade head
```

## Production Notes

- Set strong `SECRET_KEY` and `POSTGRES_PASSWORD`.
- Replace mock notification channels with provider integrations.
- Mount persistent storage for `backend/storage`.
- Use HTTPS reverse proxy (Nginx/Traefik).
