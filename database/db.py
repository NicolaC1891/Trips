"""
Database connection configuration
"""

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from settings import config

db_url = config.database.DB_URL
engine = create_async_engine(url=db_url)
async_session_factory = async_sessionmaker(engine, expire_on_commit=False)