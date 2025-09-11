"""
Defines ORM data models for the bot database.

Includes the following table mappings:
- MessageMenu: stores response texts for menu messages and commands
- CatPhrase: stores randomly selected phrases spoken by the Office Cat
- ReportReminder: stores user reminders for advance report submission deadlines

Built using SQLAlchemy with async support. Models inherit from (DeclarativeBase + AsyncAttrs).
"""

from datetime import date

from sqlalchemy import Integer, Date, Text
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True


class MenuItem(Base):
    """
    Stores predefined response texts for menu options and feature entrypoints.

    Fields:
    - key: string identifier (command, keyword, or message trigger)
    - response: text shown to the user as a reply
    """

    __tablename__ = "menu"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    key: Mapped[str]
    response: Mapped[str]
    children: Mapped[str]
    prev: Mapped[str]
    next_: Mapped[str]
    parent: Mapped[str]
    label: Mapped[str]


class HomeFlowStep(Base):
    __tablename__ = "home"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    key: Mapped[str]
    response: Mapped[str]
    children: Mapped[str]
    prev: Mapped[str]
    next_: Mapped[str]
    parent: Mapped[str]
    label: Mapped[str]

class AbroadFlowStep(Base):
    __tablename__ = "abroad"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    key: Mapped[str]
    response: Mapped[str]
    children: Mapped[str]
    prev: Mapped[str]
    next_: Mapped[str]
    parent: Mapped[str]
    label: Mapped[str]

class RepexpFlowStep(Base):
    __tablename__ = "repexp"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    key: Mapped[str]
    response: Mapped[str]
    children: Mapped[str]
    prev: Mapped[str]
    next_: Mapped[str]
    parent: Mapped[str]
    label: Mapped[str]


class AdvanceItem(Base):
    __tablename__ = "advance"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    key: Mapped[str]
    response: Mapped[str]
    children: Mapped[str]
    prev: Mapped[str]
    next_: Mapped[str]
    parent: Mapped[str]
    label: Mapped[str]


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
    return_date: Mapped[date] = mapped_column(Date)
    reminder_date: Mapped[date] = mapped_column(Date)
    report_deadline: Mapped[date] = mapped_column(Date)


class CatWisdom(Base):
    """
    Stores randomly selected phrases spoken by the Office Cat bot.
    Used to create emotional connection between users and the bot.

    Fields:
    - phrase: a single text phrase to be selected at random
    """

    __tablename__ = "cat_wisdom"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    wisdom: Mapped[str]


class AIChunk(Base):
    __tablename__ = 'chunks'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    chunk_text: Mapped[str] = mapped_column(Text)
    category: Mapped[str] = mapped_column(Text)  # общая категория по сущностям
    topic: Mapped[str] = mapped_column(Text, nullable=True)  # действия с сущностями
    flow_item: Mapped[str] = mapped_column(Text, nullable=True)   # пункт флоу для референса
