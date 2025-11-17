# Backend Setup Guide

Comprehensive setup guide for the LangGraph Python/FastAPI backend.

## Prerequisites

- **Python 3.11 or higher**
- **PostgreSQL** running on port 5434 (or configure your own)
- **Git** (for cloning)

## Step 1: Environment Setup

### 1.1 Create Virtual Environment

```bash
cd backend
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 1.2 Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Step 2: Database Setup

### 2.1 Start PostgreSQL

If using Docker (recommended):

```bash
cd ../frontend
docker compose up -d
```

This starts PostgreSQL on port 5434.

### 2.2 Create Database

The database will be created automatically on first run if using the frontend's docker-compose setup.

Alternatively, create manually:

```bash
createdb -h localhost -p 5434 -U postgres langgraph_agent
```

## Step 3: Configuration

### 3.1 Create .env File

```bash
cp .env.template .env
```

### 3.2 Configure Environment Variables

Edit `.env` and add your API keys:

```env
# Required: Add your LLM API keys
OPENAI_API_KEY=sk-your-actual-openai-key
GOOGLE_API_KEY=your-actual-google-key

# Optional: Customize these
DATABASE_URL=postgresql://postgres:postgres@localhost:5434/langgraph_agent
PORT=8000
CORS_ORIGINS=http://localhost:3000
```

## Step 4: Initialize Database

The application will automatically create tables on first run in development mode.

To verify database connection:

```bash
python -c "from app.database import engine; import asyncio; asyncio.run(engine.connect())"
```

## Step 5: Run the Application

### Development Mode (with auto-reload):

```bash
python run.py
```

Or with uvicorn directly:

```bash
uvicorn app.main:app --reload --port 8000
```

The API will be available at: `http://localhost:8000`

### API Documentation

Once running, access the interactive API docs:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Step 6: Run Tests

### Run all tests:

```bash
pytest
```

### Run with coverage:

```bash
pytest --cov=app --cov-report=html
```

View coverage report at `htmlcov/index.html`

### Run specific test file:

```bash
pytest tests/test_api_threads.py -v
```

## Step 7: Verify Installation

Test the health endpoint:

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

## Common Issues and Solutions

### Issue: Database Connection Failed

**Solution**: Verify PostgreSQL is running:
```bash
psql -h localhost -p 5434 -U postgres -d langgraph_agent
```

### Issue: Import Errors

**Solution**: Ensure virtual environment is activated and dependencies installed:
```bash
pip install -r requirements.txt
```

### Issue: Port Already in Use

**Solution**: Change port in `.env`:
```env
PORT=8001
```

### Issue: CORS Errors

**Solution**: Add your frontend URL to CORS_ORIGINS in `.env`:
```env
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

## Development Workflow

### Code Formatting

```bash
# Format code
black app tests

# Check formatting
black --check app tests
```

### Linting

```bash
# Lint with ruff
ruff check app tests

# Auto-fix issues
ruff check --fix app tests
```

### Type Checking

```bash
mypy app
```

### Database Migrations (Optional)

If you need to make schema changes:

```bash
# Create migration
alembic revision --autogenerate -m "Description"

# Apply migration
alembic upgrade head
```

## Production Deployment

For production deployment:

1. Set `ENVIRONMENT=production` in `.env`
2. Use proper secrets management (not `.env` files)
3. Use a production WSGI server:

```bash
gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

4. Configure proper database connection pooling
5. Set up monitoring and logging
6. Use HTTPS/TLS

## Next Steps

- Review the [Architecture Documentation](../.cursor/rules/arquitecture.md)
- Check out the [API Documentation](http://localhost:8000/docs) after starting the server
- Configure MCP servers via the API or frontend
- Start building your agent workflows!

## Support

For issues or questions:
- Check the [README.md](./README.md)
- Review test examples in `tests/`
- Examine the frontend integration in `../frontend/`

