"""Script to run the FastAPI application."""

import sys
import asyncio
import uvicorn
from app.config import settings

# Fix para Windows: usar SelectorEventLoop para compatibilidad con psycopg async
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level.lower(),
    )

