import pytest
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from cat_bot.daily_wisdom import get_today_wisdom
from database.models import Base, CatPhrase


@pytest.fixture(scope="module")
async def make_test_session():
    engine = create_async_engine(
        url="sqlite+aiosqlite:///:memory:"
    )  # create live engine with in-memory db
    async with engine.begin() as connection:  # open connection
        await connection.run_sync(Base.metadata.create_all)
        session_maker = async_sessionmaker(engine)  # create session factory
        yield session_maker
    # teardown
    await engine.dispose()


@pytest.mark.asyncio
async def test_cat_silent_if_table_empty(make_test_session):
    async with make_test_session() as session:
        await session.execute(delete(CatPhrase))
        await session.commit()
        # test
        await session.execute(select(CatPhrase.id))
        result = await get_today_wisdom(session)
        assert result == "Кот сегодня молчит..."


@pytest.mark.asyncio
async def test_cat_speaks_if_phrase_available(make_test_session):
    async with make_test_session() as session:
        phrases = ("Мяу раз", "Мяу два")
        for phrase in phrases:
            session.add(CatPhrase(phrase=phrase))
        await session.flush()
        # test
        result = await get_today_wisdom(session)
        assert result in phrases
        # teardown
        await session.execute(delete(CatPhrase))
        await session.commit()
