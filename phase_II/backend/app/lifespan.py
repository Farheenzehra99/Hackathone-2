import asyncio
from app.db.base import create_db_and_tables
from app.main import app

async def lifespan(app):
    # Initialize database tables on startup
    await create_db_and_tables()
    yield
    # Cleanup on shutdown if needed

app.lifespan = lifespan