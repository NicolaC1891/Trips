"""
Database engine and asynchronous session factory configuration.

This module initializes the SQLAlchemy async engine using the database URL
from the project environment settings and provides a reusable session factory for
performing asynchronous database operations throughout the application.

Exports:
- `engine`: SQLAlchemy async engine instance
- `async_session_factory`: async session maker for database access
"""

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from settings import config

db_url = config.database.DB_URL
engine = create_async_engine(url=db_url)
async_session_factory = async_sessionmaker(engine, expire_on_commit=False)
