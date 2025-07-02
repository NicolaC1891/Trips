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


class MessageBel(Base):
    __tablename__: str = 'msg_bel'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    key: Mapped[str]
    answer: Mapped[str]    # nullable False by default


class MessageRus(Base):
    __tablename__: str = 'msg_rus'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    key: Mapped[str]
    answer: Mapped[str]    # nullable False by default
