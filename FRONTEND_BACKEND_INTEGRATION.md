# Frontend-Backend Integration Guide

Guide for connecting the Next.js frontend with the Python/FastAPI backend.

## Overview

The Python backend has been designed to be **100% API-compatible** with the original Next.js backend. This means the frontend can connect to either backend without code changes.

## Configuration

### Option 1: Environment Variable (Recommended)

Create or update `frontend/.env.local`:

```env
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# Or for production:
# NEXT_PUBLIC_API_URL=https://your-backend-domain.com
```

### Option 2: Next.js Configuration

Update `frontend/next.config.ts` to add API rewrites:

```typescript
const nextConfig = {
  // ... existing config
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8000/api/:path*',
      },
    ]
  },
}
```

## Running Both Services

### Terminal 1: Backend (Python/FastAPI)

```bash
cd backend

# Activate virtual environment (if not activated)
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Run backend
python run.py
```

Backend will run on: **http://localhost:8000**

### Terminal 2: Database (PostgreSQL)

```bash
cd frontend
docker compose up -d
```

Database will run on: **localhost:5434**

### Terminal 3: Frontend (Next.js)

```bash
cd frontend
pnpm dev
```

Frontend will run on: **http://localhost:3000**

## API Endpoint Mapping

All endpoints remain the same:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/agent/stream` | GET | Stream agent responses (SSE) |
| `/api/agent/history/{threadId}` | GET | Get thread history |
| `/api/agent/threads` | GET | List threads |
| `/api/agent/threads` | POST | Create thread |
| `/api/agent/threads/{id}` | GET | Get thread |
| `/api/agent/threads/{id}` | PUT | Update thread |
| `/api/agent/threads/{id}` | DELETE | Delete thread |
| `/api/mcp-servers` | GET | List MCP servers |
| `/api/mcp-servers` | POST | Create MCP server |
| `/api/mcp-servers/{id}` | GET | Get MCP server |
| `/api/mcp-servers/{id}` | PUT | Update MCP server |
| `/api/mcp-servers/{id}` | DELETE | Delete MCP server |
| `/api/mcp-tools` | GET | List available tools |

## CORS Configuration

The backend is pre-configured to accept requests from:
- `http://localhost:3000`
- `http://localhost:3001`

To add more origins, update `backend/.env`:

```env
CORS_ORIGINS=http://localhost:3000,http://localhost:3001,https://your-domain.com
```

## Testing the Connection

### 1. Test Backend Health

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "environment": "development"
}
```

### 2. Test API Docs

Visit: http://localhost:8000/docs

You should see the interactive Swagger UI with all endpoints.

### 3. Test from Frontend

Open the frontend at http://localhost:3000 and:

1. Create a new thread
2. Send a message
3. Check that responses stream correctly
4. Verify MCP servers can be added/edited

## Troubleshooting

### CORS Errors

**Symptom:** Browser console shows CORS errors

**Solution:** 
1. Verify backend is running
2. Check `CORS_ORIGINS` in backend `.env`
3. Ensure frontend URL is included in CORS origins

### Connection Refused

**Symptom:** `ECONNREFUSED` errors

**Solution:**
1. Ensure backend is running: `python run.py`
2. Verify port 8000 is not in use
3. Check firewall settings

### SSE Streaming Issues

**Symptom:** Messages don't stream, or streaming stops

**Solution:**
1. Check browser console for errors
2. Verify SSE endpoint: `curl http://localhost:8000/api/agent/stream?content=test&threadId=test`
3. Ensure API keys are configured in backend `.env`

### Database Connection Errors

**Symptom:** Backend logs show database connection errors

**Solution:**
1. Start PostgreSQL: `docker compose up -d` (in frontend folder)
2. Verify connection: `psql -h localhost -p 5434 -U postgres`
3. Check `DATABASE_URL` in backend `.env`

## Development Tips

### Hot Reload

Both services support hot reload:
- **Backend**: Uses `uvicorn --reload` (automatically restarts on code changes)
- **Frontend**: Uses Next.js Fast Refresh (automatically updates on save)

### Debugging

**Backend Logs:**
- Check terminal running `python run.py`
- Logs show all HTTP requests and database queries
- Set `LOG_LEVEL=DEBUG` in `.env` for more details

**Frontend Logs:**
- Browser DevTools Console
- Network tab for API requests
- React DevTools for component state

### API Testing

Use the Swagger UI for quick API testing:
1. Visit http://localhost:8000/docs
2. Click on any endpoint
3. Click "Try it out"
4. Fill in parameters
5. Click "Execute"

## Production Deployment

### Backend

1. Set environment variables (not `.env` file)
2. Use production WSGI server:
   ```bash
   gunicorn app.main:app \
     --workers 4 \
     --worker-class uvicorn.workers.UvicornWorker \
     --bind 0.0.0.0:8000
   ```
3. Use proper database connection pooling
4. Enable HTTPS/TLS
5. Configure proper CORS origins

### Frontend

1. Build production bundle:
   ```bash
   cd frontend
   pnpm build
   ```
2. Update API URL to production backend
3. Deploy to Vercel, Netlify, or your hosting

### Database

1. Use managed PostgreSQL (AWS RDS, DigitalOcean, etc.)
2. Configure connection pooling
3. Enable SSL connections
4. Regular backups

## Migration Checklist

- [ ] Backend running on port 8000
- [ ] Database running on port 5434
- [ ] Frontend running on port 3000
- [ ] Backend health check passing
- [ ] Frontend can create threads
- [ ] Frontend can send messages
- [ ] SSE streaming working
- [ ] MCP servers can be managed
- [ ] Tool approval workflow working

## Next Steps

1. Configure your LLM API keys in `backend/.env`
2. Start all three services (database, backend, frontend)
3. Test the complete workflow
4. Add MCP servers via the UI
5. Start building your agent!

## Support

For issues:
- Check backend logs in terminal
- Check frontend console in browser
- Review API docs at http://localhost:8000/docs
- Consult [SETUP.md](backend/SETUP.md)
- Review [MIGRATION_SUMMARY.md](backend/MIGRATION_SUMMARY.md)

