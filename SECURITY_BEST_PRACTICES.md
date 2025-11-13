# 🔒 Security Best Practices

## API Keys - IMPORTANTE

### ✅ Correcto: API Keys en el Backend

```
backend/.env (SEGURO - servidor privado)
├── OPENAI_API_KEY=sk-...
├── GOOGLE_API_KEY=...
└── DATABASE_URL=postgresql://...
```

**Por qué es seguro:**
- ✅ Las claves NUNCA se envían al navegador
- ✅ Solo el servidor Python tiene acceso
- ✅ No están expuestas en el código del cliente
- ✅ No aparecen en el bundle de JavaScript

### ❌ Incorrecto: API Keys en el Frontend

```
frontend/.env (INSEGURO - se expone al navegador)
├── NEXT_PUBLIC_API_KEY=sk-...  ❌ NUNCA HACER ESTO
└── API_KEY=sk-...              ❌ Visible en el bundle
```

**Por qué es peligroso:**
- ❌ Cualquiera puede ver las claves en DevTools
- ❌ Las claves se incluyen en el bundle JavaScript
- ❌ Se pueden extraer del código fuente
- ❌ Riesgo de uso no autorizado / cargos

## Arquitectura de Seguridad

```
┌─────────────────────────────────────┐
│  Navegador (Cliente)                │
│  - NO tiene API keys               │
│  - Solo UI y llamadas HTTP         │
└────────────┬────────────────────────┘
             │
             │ HTTP/HTTPS
             │ (sin credenciales)
             ▼
┌─────────────────────────────────────┐
│  Frontend Next.js (Puerto 3000)     │
│  - Proxy simple                    │
│  - NO ejecuta lógica de IA         │
│  - Solo reenvía peticiones         │
└────────────┬────────────────────────┘
             │
             │ HTTP interno
             │
             ▼
┌─────────────────────────────────────┐
│  Backend Python (Puerto 8000)       │
│  ✅ API Keys almacenadas aquí     │
│  ✅ Lógica de LangGraph           │
│  ✅ Llamadas a OpenAI/Google      │
└─────────────────────────────────────┘
```

## Variables de Entorno

### Backend (`backend/.env`)

```env
# ✅ API Keys aquí (servidor privado)
OPENAI_API_KEY=sk-tu-clave-real-aqui
GOOGLE_API_KEY=tu-clave-real-aqui

# ✅ Configuración del servidor
DATABASE_URL=postgresql://user:password@localhost:5434/mydb
PORT=8000
CORS_ORIGINS=http://localhost:3000
```

### Frontend (`frontend/.env`)

```env
# ✅ Solo URLs públicas y configuración no sensible
NEXT_PUBLIC_API_URL=http://localhost:8000
DATABASE_URL=postgresql://user:password@localhost:5434/mydb

# ❌ NO poner API keys aquí
# OPENAI_API_KEY=...  ❌ NUNCA
```

## Reglas de Oro

### 1. Variables con `NEXT_PUBLIC_`

En Next.js, cualquier variable que empiece con `NEXT_PUBLIC_` se expone al navegador:

```env
# ❌ PELIGRO: Se expone al navegador
NEXT_PUBLIC_OPENAI_KEY=sk-...

# ✅ SEGURO: Solo URL pública del backend
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 2. Variables sin `NEXT_PUBLIC_`

Las variables sin este prefijo solo están disponibles en el servidor de Next.js:

```env
# ✅ Más seguro (solo server-side)
DATABASE_URL=postgresql://...

# ⚠️ Pero aún así, mejor en backend Python
OPENAI_API_KEY=sk-...
```

### 3. Arquitectura Recomendada

```
Frontend:
  ├── Variables públicas (NEXT_PUBLIC_*)
  └── Database URL (solo para Prisma server-side)

Backend Python:
  ├── ✅ API Keys (OpenAI, Google, etc.)
  ├── ✅ Database URL
  └── ✅ Secretos sensibles
```

## Checklist de Seguridad

Antes de desplegar a producción:

- [ ] **API keys solo en backend**
- [ ] **No hay API keys en `frontend/.env`**
- [ ] **No hay API keys en el código fuente**
- [ ] **`.env` en `.gitignore`**
- [ ] **Backend usa HTTPS en producción**
- [ ] **CORS configurado correctamente**
- [ ] **Variables de entorno en servicio de hosting** (no en archivos)
- [ ] **Rate limiting en backend**
- [ ] **Autenticación para usuarios** (si es pública)

## Despliegue en Producción

### Backend Python

```bash
# ❌ NUNCA hacer esto
git add backend/.env

# ✅ Configurar en el servicio de hosting
# Vercel, Heroku, AWS, etc.
# Variables de entorno → OpenAI_API_KEY=...
```

### Frontend Next.js

```bash
# ✅ Variables públicas en build time
NEXT_PUBLIC_API_URL=https://api.tudominio.com

# ❌ NUNCA incluir API keys
```

## ¿Por qué este diseño?

### Ventajas de API Keys en Backend:

1. **Seguridad**: Las claves nunca llegan al navegador
2. **Control**: Puedes implementar rate limiting
3. **Monitoreo**: Logs centralizados de uso de IA
4. **Costos**: Control de cuántas requests se hacen
5. **Rotación**: Cambiar claves sin rebuild del frontend
6. **Multi-tenant**: Diferentes usuarios, mismas claves

### Desventajas de API Keys en Frontend:

1. ❌ Cualquiera puede extraer las claves
2. ❌ Uso no autorizado
3. ❌ Costos inesperados
4. ❌ No puedes revocar el acceso
5. ❌ Difícil de actualizar (requiere rebuild)

## Respuesta a tu Pregunta

> "¿Las API keys tienen que estar en el .env del frontend para actualizarlas más fácil?"

**NO.** Es exactamente al revés:

- ✅ **Backend**: Actualizar `.env` → reiniciar servidor (segundos)
- ❌ **Frontend**: Actualizar → rebuild → redeploy (minutos)

Además, en producción:
- Backend: Variables de entorno del hosting (instantáneo)
- Frontend: Rebuild y redeploy completo del sitio

## Conclusión

```
┌─────────────────────────────────────────────┐
│  📱 Frontend                                │
│  - Solo UI                                 │
│  - Hace peticiones HTTP                    │
│  - NO tiene API keys                       │
│  - NO ejecuta lógica de IA                 │
└─────────────────────────────────────────────┘
                    ⬇️
┌─────────────────────────────────────────────┐
│  🔒 Backend (Python)                       │
│  ✅ API Keys seguras                       │
│  ✅ Lógica de LangGraph                    │
│  ✅ Control total                          │
└─────────────────────────────────────────────┘
```

**Las API keys SIEMPRE en el backend. Nunca en el frontend.**

