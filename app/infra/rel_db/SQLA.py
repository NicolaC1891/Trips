"""
Defines ORM data models for the bot database.

Includes the following table mappings:
- MessageMenu: stores response texts for menu messages and commands
- CatPhrase: stores randomly selected phrases spoken by the Office Cat
- ReportReminder: stores user reminders for advance report submission deadlines

Built using SQLAlchemy with async support. Models inherit from (DeclarativeBase + AsyncAttrs).
"""

from datetime import date

from sqlalchemy import Integer, Date, Text, UniqueConstraint, String
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True


class FlowStepBase(Base):
    __abstract__ = True
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    key: Mapped[str] = mapped_column(String)
    response: Mapped[str] = mapped_column(String)
    children: Mapped[str] = mapped_column(String)
    prev: Mapped[str] = mapped_column(String)
    next_: Mapped[str] = mapped_column(String)
    parent: Mapped[str] = mapped_column(String)
    label: Mapped[str] = mapped_column(String)


class MenuItem(FlowStepBase):
    __tablename__ = "menu"


class HomeFlow(FlowStepBase):
    __tablename__ = "home"


class AbroadFlow(FlowStepBase):
    __tablename__ = "abroad"


class RepexpFlow(FlowStepBase):
    __tablename__ = "repexp"


class AdvanceItem(FlowStepBase):
    __tablename__ = "advance"


class PlannerFlow(FlowStepBase):
    __tablename__ = "planner"

class TimesheetFlow(FlowStepBase):
    __tablename__ = "timesheet"


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


class UserStats(Base):
    __tablename__ = "user_stats"
    __table_args__ = (UniqueConstraint('user_id', 'feature_name', 'log_date', name='uix_user_feature_date'), )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int]
    feature_name: Mapped[str]
    log_date: Mapped[date]


class PlannerCities(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    cityname: Mapped[int]
    region: Mapped[str]
    city: Mapped[str]
    hotel: Mapped[str]
    lat: Mapped[float]
    lon: Mapped[float]


