import os
from settings import config
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

db_url = f"sqlite+aiosqlite:///{config.database.DB_URL}"

engine = create_async_engine(url=db_url)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)    # сейчас БД хранит, не обновляется
