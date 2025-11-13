# 🚀 Quick Start - 5 Minutos hasta estar funcionando

## TL;DR

```bash
# 1. Base de datos
cd frontend && docker compose up -d

# 2. Backend (nueva terminal)
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
# Editar .env con tus API keys
python run.py

# 3. Frontend (nueva terminal)
cd frontend && pnpm dev

# Listo! → http://localhost:3000
```

## 📋 Paso a Paso

### 1️⃣ Base de Datos (30 segundos)

```bash
cd frontend
docker compose up -d
```

✅ PostgreSQL corriendo en puerto 5434

### 2️⃣ Backend Python (2 minutos)

```bash
cd backend

# Crear entorno virtual
python -m venv venv

# Activar (Windows)
venv\Scripts\activate

# Activar (macOS/Linux)
source venv/bin/activate

# Instalar
pip install -r requirements.txt
```

**Importante**: Crear/editar `backend/.env`:
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5434/langgraph_agent
OPENAI_API_KEY=sk-tu-api-key-aqui
PORT=8000
CORS_ORIGINS=http://localhost:3000
```

```bash
# Ejecutar
python run.py
```

✅ Backend corriendo en http://localhost:8000  
✅ API Docs en http://localhost:8000/docs

### 3️⃣ Frontend (1 minuto)

```bash
cd frontend
pnpm install
pnpm dev
```

✅ Frontend corriendo en http://localhost:3000

## ✅ Verificación

1. **Backend**: http://localhost:8000/health → `{"status":"healthy"}`
2. **API Docs**: http://localhost:8000/docs → Swagger UI
3. **Frontend**: http://localhost:3000 → Interfaz carga
4. **Crear thread** → Enviar mensaje → Ver respuesta streaming ✨

## 🐛 Troubleshooting Rápido

| Problema | Solución |
|----------|----------|
| Puerto 8000 ocupado | Cambiar `PORT=8001` en `.env` |
| Error de conexión DB | `docker compose up -d` en `frontend/` |
| Import errors | `pip install -r requirements.txt` |
| CORS errors | Verificar `CORS_ORIGINS` en `.env` |
| "No API key" | Agregar `OPENAI_API_KEY` en `.env` |

## 📚 Más Info

- **Documentación completa**: [PLAN_COMPLETO_Y_RESUMEN.md](PLAN_COMPLETO_Y_RESUMEN.md)
- **Setup detallado**: [backend/SETUP.md](backend/SETUP.md)
- **Integración frontend**: [FRONTEND_BACKEND_INTEGRATION.md](FRONTEND_BACKEND_INTEGRATION.md)
- **Migración técnica**: [backend/MIGRATION_SUMMARY.md](backend/MIGRATION_SUMMARY.md)

## 🎉 ¡Eso es todo!

El sistema completo (base de datos, backend Python, frontend Next.js) debería estar funcionando.

**Siguiente**: Agregar servidores MCP desde la UI y empezar a construir tu agente! 🤖

