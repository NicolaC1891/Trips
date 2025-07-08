"""
Defines ORM data models for the bot database.

Includes the following table mappings:
- MessageMenu: stores response texts for menu messages and commands
- CatPhrase: stores randomly selected phrases spoken by the Office Cat
- ReportReminder: stores user reminders for advance report submission deadlines

Built using SQLAlchemy with async support. Models inherit from (DeclarativeBase + AsyncAttrs).
"""

from datetime import datetime

from sqlalchemy import DateTime, Integer
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True


class MessageMenu(Base):
    """
    Stores predefined response texts for menu commands or keywords.

    Fields:
    - key: string identifier (command, keyword, or message trigger)
    - response: text shown to the user as a reply
    """

    __tablename__ = "msg_menu"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    key: Mapped[str]
    response: Mapped[str]  # nullable False by default


class CatPhrase(Base):
    """
    Stores randomly selected phrases spoken by the Office Cat bot.
    Used to create emotional connection between users and the bot.

    Fields:
    - phrase: a single text phrase to be selected at random
    """

    __tablename__ = "cat_phrase"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    phrase: Mapped[str]


class ReportReminder(Base):
    """
    Stores user reminders related to advance report submission deadlines.

    Fields:
    - user_id: Telegram user ID
    - return_date: the user's selected return date from the business trip
    - reminder_date: when the bot should remind the user to submit the advance report
    - report_deadline: the final day to submit the advance report
    """

    __tablename__ = "rep_reminder"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int]
    return_date: Mapped[datetime] = mapped_column(DateTime)
    reminder_date: Mapped[datetime] = mapped_column(DateTime)
    report_deadline: Mapped[datetime] = mapped_column(DateTime)
