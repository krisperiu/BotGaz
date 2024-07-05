from sqlalchemy import BigInteger, String, ForeignKey, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

import datetime as dt
import os
from dotenv import load_dotenv

load_dotenv()
engine = create_async_engine(url=os.getenv('SQLALCHEMY_URL'))

async_session = async_sessionmaker(engine)

class Base (AsyncAttrs, DeclarativeBase):
    pass

class Admin(Base):
    __tablename__ = 'admins'
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    level: Mapped[int] = mapped_column(autoincrement = 1)

class Report(Base):
    __tablename__ = 'reports'
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    appearance: Mapped[str] = mapped_column(String(15))
    cl_interior: Mapped[str] = mapped_column(String(15))
    cl_seat: Mapped[str] = mapped_column(String(15))
    cl_handles: Mapped[str] = mapped_column(String(15))
    seat_integrity: Mapped[str] = mapped_column(String(15))
    checklist: Mapped[str] = mapped_column(String(15))
    portfolio: Mapped[str] = mapped_column(String(15))
    seat_belts: Mapped[str] = mapped_column(String(15))
    drivers_appearance: Mapped[str] = mapped_column(String(15))
    behaviour: Mapped[str] = mapped_column(String(15))
    briefing: Mapped[str] = mapped_column(String(15))
    temperature: Mapped[str] = mapped_column(String(15))
    comment: Mapped[str] = mapped_column(String(250))
    ranked: Mapped[int] = mapped_column()
    state_number: Mapped[str] = mapped_column(String(10), ForeignKey('buses.state_number'))
    date: Mapped[dt.date] = mapped_column(Date)
    status: Mapped[int] = mapped_column()
    comment_moder: Mapped[str] = mapped_column(String(250))

class Bus(Base):
    __tablename__ = 'buses'
    state_number: Mapped[str] = mapped_column(String(10), primary_key=True)
    bus_info: Mapped[str] = mapped_column(String(80))

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)