from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlmodel import SQLModel
from app.core.config import settings
import ssl

# Ensure asyncpg URL
assert settings.DATABASE_URL.startswith("postgresql+asyncpg://"), \
    "DATABASE_URL must start with postgresql+asyncpg://"

# SSL context for Neon PostgreSQL
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

connect_args = {"ssl": ssl_context}

engine: AsyncEngine = create_async_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    echo=settings.DEBUG,
)

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
