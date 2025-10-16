# Frontend - Monitoring App

## Snabbstart

### Lokal utveckling

```bash
cd frontend
npm install
npm run dev
```

### Docker

```bash
docker compose up --build
```

## Konfiguration

### API URL

Ändra URL i `src/config.ts`:

```typescript
export const API_URL = "http://python-chasacademy.local:3000";
```

**För lokal testning:** Ändra till `http://localhost:3000`

## Teknisk Stack

- **SvelteKit** + **Vite** + **TypeScript**
- **Docker** med **Nginx** container
- **Nginx proxy** routar API-anrop till backend

## Funktioner

- Meny-system
- Övervakning (CPU, RAM, Disk)
- Larm-system
- Realtidsstatus

## Docker Struktur

- `frontend` container: Serves SvelteKit-app
- `nginx` container: Proxy på port 3000
- `backend` container: API på port 8000
