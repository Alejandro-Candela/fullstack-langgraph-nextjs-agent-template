# LangGraph Agent Backend (FastAPI)

Backend implementation of the LangGraph.js AI Agent Template using Python, FastAPI, and LangGraph.

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL running on port 5434
- Poetry or pip for dependency management

### Installation

1. **Install dependencies:**

```bash
cd backend
pip install -r requirements.txt
```

2. **Configure environment variables:**

Create a `.env` file in the `backend/` directory:

```bash
# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5434/langgraph_agent
DB_SSLMODE=disable

# LLM API Keys
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_API_KEY=your_google_api_key_here

# Server
HOST=0.0.0.0
PORT=8000
RELOAD=true

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# Environment
ENVIRONMENT=development
LOG_LEVEL=INFO
```

3. **Initialize database:**

The database tables will be created automatically on first run in development mode.

4. **Run the server:**

```bash
python -m app.main
```

Or with uvicorn directly:

```bash
uvicorn app.main:app --reload --port 8000
```

## 📁 Project Structure

```
backend/
├── app/
│   ├── agent/              # LangGraph agent logic
│   │   ├── builder.py      # Agent StateGraph builder
│   │   ├── mcp.py          # MCP integration
│   │   ├── memory.py       # Checkpointer and history
│   │   └── prompt.py       # System prompts
│   ├── models/             # SQLAlchemy models
│   │   ├── thread.py       # Thread model
│   │   └── mcp_server.py   # MCP server config model
│   ├── schemas/            # Pydantic schemas
│   │   ├── message.py      # Message types
│   │   ├── thread.py       # Thread schemas
│   │   └── mcp.py          # MCP schemas
│   ├── routers/            # API endpoints
│   │   ├── agent.py        # Agent endpoints (stream, history)
│   │   ├── threads.py      # Thread CRUD
│   │   └── mcp_servers.py  # MCP server CRUD
│   ├── services/           # Business logic
│   │   ├── agent_service.py    # Agent streaming service
│   │   └── thread_service.py   # Thread management
│   ├── config.py           # Configuration
│   ├── database.py         # Database setup
│   └── main.py             # FastAPI app
├── tests/                  # Test suite
│   ├── test_agent.py
│   ├── test_mcp.py
│   └── test_api.py
├── requirements.txt
├── pytest.ini
└── pyproject.toml
```

## 🧪 Testing

Run tests with pytest:

```bash
pytest
```

With coverage:

```bash
pytest --cov=app --cov-report=html
```

## 🔧 Development

### Code Formatting

```bash
# Format with black
black app tests

# Lint with ruff
ruff check app tests

# Type check with mypy
mypy app
```

### API Documentation

Once the server is running, access:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 📡 API Endpoints

### Agent
- `GET /api/agent/stream` - Stream agent responses (SSE)
- `GET /api/agent/history/{threadId}` - Get thread history

### Threads
- `GET /api/agent/threads` - List all threads
- `POST /api/agent/threads` - Create new thread
- `GET /api/agent/threads/{id}` - Get thread details
- `PUT /api/agent/threads/{id}` - Update thread
- `DELETE /api/agent/threads/{id}` - Delete thread

### MCP Servers
- `GET /api/mcp-servers` - List all MCP servers
- `POST /api/mcp-servers` - Create new MCP server
- `GET /api/mcp-servers/{id}` - Get MCP server details
- `PUT /api/mcp-servers/{id}` - Update MCP server
- `DELETE /api/mcp-servers/{id}` - Delete MCP server
- `GET /api/mcp-tools` - List available MCP tools

## 🏗️ Architecture

This backend follows the principles outlined in the architecture documentation:

- **FastAPI** for high-performance async API
- **LangGraph** for agent orchestration with human-in-the-loop
- **PostgreSQL** for data persistence and checkpointing
- **SQLAlchemy** for ORM and database access
- **Pydantic** for request/response validation
- **SSE** for real-time streaming responses

### Key Components

1. **Agent Builder**: Creates StateGraph with agent→tool_approval→tools flow
2. **MCP Integration**: Dynamically loads tools from MCP servers in database
3. **Streaming Service**: Generates async SSE stream for real-time responses
4. **Checkpointer**: Uses LangGraph's PostgreSQL checkpointer for conversation history

## 🔄 Migration from Next.js Backend

This backend is a direct Python port of the original Next.js implementation:

- Maintains the same API contract for frontend compatibility
- Uses the same database schema (Thread, MCPServer)
- Implements the same agent workflow (human-in-the-loop tool approval)
- Provides SSE streaming with identical message format

## 📚 Related Documentation

- [Architecture Documentation](../.cursor/rules/arquitecture.md)
- [Project Overview](../.cursor/rules/project.md)
- [Frontend README](../frontend/README.md)

