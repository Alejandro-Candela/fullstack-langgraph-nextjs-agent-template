# Fullstack LangGraph (Python) + Next.js Agent Template

Production-ready template for building AI agents with **LangGraph (Python)** on the backend and **Next.js** on the frontend. Features **persistent memory**, **real-time streaming**, **conversation thread management**, and a **modern UI** for agent interaction.

---

## ✨ Features

- **Agent Orchestration with LangGraph (Python)**  
  State graph, checkpoints, and *human‑in‑the‑loop* (interrupts / resumes) for secure and auditable flows.
- **Real-time Streaming (SSE)**  
  Token-by-token responses and agent events streamed to the Next.js frontend.
- **Persistent Memory & Threads**  
  History per conversation/thread and state resumption from LangGraph checkpoints.
- **Modern UI with Next.js**  
  Chat interface with state management, reconnection, and error handling.
- **Production Ready**  
  Environment variables, Docker for the database, migrations, and clear front/back separation.

---

## 🧱 Architecture (High Level)

```
[ Next.js (Frontend) ]  <──SSE/HTTP──>  [ Backend Python (LangGraph) ]  <──>  [ DB / Vector Store ]
        Chat UI                               Agent Orchestration                Persistence
   (React / Tailwind)                         State + Checkpoints             (PostgreSQL, etc.)
```

---

## 📦 Requirements

- **Backend**: Python 3.11+ (or your preferred version), dependency manager (uv/poetry/pip).  
- **Frontend**: Node.js 18+ and pnpm (or npm/yarn).  
- **Database**: Docker for PostgreSQL (or your defined DB).  
- **AI Providers**: OpenAI / Google keys (optional depending on config).

---

## ⚙️ Environment Configuration

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

## 🗄️ Database (Docker) - **IMPORTANT**

> [!IMPORTANT]
> You **MUST** start the Docker containers for the database before running the backend. The backend depends on the database to function.

```bash
cd backend
docker compose up -d
```

---

## ▶️ Getting Started

### Backend
```bash
cd backend
# Ensure Docker is running (see above)
uv sync            # or: pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend
```bash
cd frontend
pnpm install
pnpm dev
```

---

## 🧠 Agent Flow (LangGraph)

1. User sends input from the UI.
2. LangGraph graph processes state, calls LLMs/tools, and emits events via SSE.
3. Next.js frontend renders in real-time and enables *human‑in‑the‑loop*.

---

## 🧩 Repository Structure
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

## 🧪 Development Commands

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

## 🔒 Security & Production

- Keep keys in environment variables.
- Enable explicit CORS.
- Use HTTPS and reverse proxy.
- Robust persistence for checkpoints.

---

## 🤝 Contributing

1. Create branch: `git checkout -b feat/my-improvement`
2. Changes + tests
3. PR with context

---

## 📄 License

MIT
