# Fullstack LangGraph (Python) + Next.js Agent Template

Template de producción para crear agentes de IA con **LangGraph (Python)** en el backend y **Next.js** en el frontend. Ofrece **memoria persistente**, **streaming en tiempo real**, **gestión de hilos de conversación**, y una **UI moderna** para interacción con el agente.

---

## ✨ Características

- **Orquestación de agentes con LangGraph (Python)**  
  Grafo de estados, checkpoints y *human‑in‑the‑loop* (interrupciones / reanudaciones) para flujos seguros y auditables.
- **Streaming en tiempo real (SSE)**  
  Respuestas token a token y eventos del agente hacia el frontend Next.js.
- **Memoria persistente e hilos**  
  Historial por conversación/hilo y reanudación del estado desde checkpoints de LangGraph.
- **UI moderna con Next.js**  
  Interfaz de chat con manejo de estados, reconexión y errores.
- **Preparado para producción**  
  Variables de entorno, Docker para la base de datos, migraciones y separación clara front/back.

---

## 🧱 Arquitectura (alto nivel)

```
[ Next.js (Frontend) ]  <──SSE/HTTP──>  [ Backend Python (LangGraph) ]  <──>  [ DB / Vector Store ]
        UI Chat                               Orquestación agente                Persistencia
   (React / Tailwind)                         Estado + Checkpoints             (PostgreSQL, etc.)
```

---

## 📦 Requisitos

- **Backend**: Python 3.11+ (o la versión que uses), gestor de dependencias (uv/poetry/pip).  
- **Frontend**: Node.js 18+ y pnpm (o npm/yarn).  
- **Base de datos**: Docker para PostgreSQL (o la que definas).  
- **Proveedores de IA**: Claves de OpenAI / Google (opcional según configuración).

---

## ⚙️ Configuración de Entorno

### Backend (`backend/.env`)
```bash
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=...
DATABASE_URL=postgresql://USER:PASSWORD@localhost:5432/agent_db
APP_PORT=8000
APP_HOST=0.0.0.0
DEFAULT_MODEL=gpt-4o-mini
```

### Frontend (`frontend/.env.local`)
```bash
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

---

## 🗄️ Base de Datos (Docker)
```bash
docker compose up -d
```

---

## ▶️ Puesta en Marcha

### Backend
```bash
cd backend
uv sync            # o: pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend
```bash
cd frontend
pnpm install
pnpm dev
```

---

## 🧠 Flujo del Agente (LangGraph)

1. Usuario envía input desde la UI.
2. Grafo LangGraph procesa estado, llama a LLMs/herramientas y emite eventos por SSE.
3. Frontend Next.js renderiza en tiempo real y permite *human‑in‑the‑loop*.

---

## 🧩 Estructura del Repositorio
```
.
├── backend/
│   ├── app/
│   │   ├── graph/
│   │   ├── api/
│   │   ├── services/
│   │   └── schemas/
│   ├── tests/
│   ├── requirements.txt / pyproject.toml
│   └── .env
├── frontend/
│   ├── app/
│   ├── components/
│   ├── lib/
│   └── .env.local
└── docker-compose.yml
```

---

## 🧪 Comandos de Desarrollo

**Backend**
```bash
ruff check . && ruff format .
pytest -q
```

**Frontend**
```bash
pnpm lint
pnpm build
```

---

## 🔒 Seguridad y Producción

- Mantén claves en variables de entorno.
- Activa CORS explícito.
- Usa HTTPS y reverse proxy.
- Persistencia robusta para checkpoints.

---

## 🤝 Contribuir

1. Crea rama: `git checkout -b feat/mi-mejora`
2. Cambios + tests
3. PR con contexto

---

## 📄 Licencia

MIT
