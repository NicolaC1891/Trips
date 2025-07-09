from datetime import datetime

import pytest
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from database.models import Base, CatPhrase, MessageMenu, ReportReminder


@pytest.fixture(scope="module")  # function or in-test teardown
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
async def test_message_menu_create_and_read(make_test_session):
    test_session = make_test_session
    async with test_session() as session:
        message_menu = MessageMenu(key="handler_key", response="response text")
        session.add(message_menu)
        await session.commit()  # Adds line to table
        query = select(MessageMenu).where(MessageMenu.key == "handler_key")
        result = await session.execute(query)  # Result object, not just dict!!!
        data = (
            result.scalar_one_or_none()
        )  # expecting one row or fail. Row is ORM object !!!
        assert data is not None
        assert data.response == "response text"
        # teardown
        await session.execute(delete(MessageMenu))  # Core SQL, faster
        await session.commit()  # because execute


@pytest.mark.asyncio
async def test_cat_phrase_create_and_read(make_test_session):
    test_session = make_test_session
    async with test_session() as session:
        cat_wisdom = CatPhrase(phrase="cat_wisdom")
        session.add(cat_wisdom)
        await session.flush()
        cat_id = cat_wisdom.id
        await session.commit()
        query = select(CatPhrase).where(CatPhrase.id == cat_id)
        result = await session.execute(query)
        data = result.scalar_one_or_none()
        assert data is not None
        assert data.phrase == "cat_wisdom"
        # teardown
        await session.execute(delete(CatPhrase))
        await session.commit()


@pytest.mark.asyncio
async def test_report_reminder_create_and_read(make_test_session):
    test_session = make_test_session
    async with test_session() as session:
        reminder = ReportReminder(
            user_id=123456,
            return_date=datetime(2025, 7, 7),
            report_deadline=datetime(2025, 7, 23),
            reminder_date=datetime(2025, 7, 22),
        )
        session.add(reminder)
        await session.commit()

        query = select(ReportReminder).where(ReportReminder.user_id == 123456)
        result = await session.execute(query)
        data = result.scalar_one_or_none()
        assert (
            isinstance(data.return_date, datetime)
            and reminder.return_date == data.return_date
        )
        assert (
            isinstance(data.report_deadline, datetime)
            and reminder.report_deadline == data.report_deadline
        )
        assert (
            isinstance(data.reminder_date, datetime)
            and reminder.reminder_date == data.reminder_date
        )
        # teardown
        await session.execute(delete(ReportReminder))
        await session.commit()


@pytest.mark.asyncio
async def test_can_store_multiple_trips_from_one_user(make_test_session):
    test_session = make_test_session
    async with test_session() as session:
        reminder_1 = ReportReminder(
            user_id=123456,
            return_date=datetime(2025, 7, 7),
            report_deadline=datetime(2025, 7, 23),
            reminder_date=datetime(2025, 7, 22),
        )
        reminder_2 = ReportReminder(
            user_id=123456,
            return_date=datetime(2025, 7, 8),
            report_deadline=datetime(2025, 7, 24),
            reminder_date=datetime(2025, 7, 23),
        )
        reminders = (reminder_1, reminder_2)
        session.add_all(reminders)
        await session.commit()

        query = (
            select(ReportReminder)
            .where(ReportReminder.user_id == 123456)
            .order_by(ReportReminder.return_date)
        )
        result = await session.execute(query)
        data = result.scalars().all()

        assert len(data) == 2  # Returning 2 rows
        assert data[0].return_date == datetime(2025, 7, 7)
        assert data[0].report_deadline == datetime(2025, 7, 23)
        assert data[0].reminder_date == datetime(2025, 7, 22)
        assert data[1].return_date == datetime(2025, 7, 8)
        assert data[1].report_deadline == datetime(2025, 7, 24)
        assert data[1].reminder_date == datetime(2025, 7, 23)

        # teardown
        await session.execute(delete(ReportReminder))
        await session.commit()
