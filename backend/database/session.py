"""
SQLAlchemy Async Database Session and Connection Lifecycle Manager
"""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from backend.core.config import settings
from backend.core.logging import get_logger

logger = get_logger("database.session")

Base = declarative_base()

async_engine = create_async_engine(
    settings.db.ASYNC_DATABASE_URL,
    echo=settings.db.POSTGRES_ECHO,
    pool_size=settings.db.POSTGRES_POOL_SIZE,
    max_overflow=settings.db.POSTGRES_MAX_OVERFLOW,
    pool_timeout=settings.db.POSTGRES_POOL_TIMEOUT,
    pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI Dependency providing an isolated asynchronous database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error_ctx("Database session rolled back due to error", exc=e)
            raise
        finally:
            await session.close()
