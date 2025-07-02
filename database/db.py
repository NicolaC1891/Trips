import os
from settings import config, BASE_DIR
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


db_url = f"sqlite+aiosqlite:///{os.path.abspath(os.path.join(BASE_DIR, config.database.DB_URL))}"

engine = create_async_engine(url=db_url)
async_session_factory = async_sessionmaker(engine, expire_on_commit=False)    # сейчас БД хранит, не обновляется
