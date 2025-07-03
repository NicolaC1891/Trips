"""
ORM data models
"""

from sqlalchemy import Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True    # Нельзя создавать экземпляры


class MessageMenu(Base):
    __tablename__: str = 'msg_menu'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    key: Mapped[str]
    answer: Mapped[str]    # nullable False by default


class CatPhrase(Base):
    __tablename__: str = 'cat_phrase'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    phrase: Mapped[str]