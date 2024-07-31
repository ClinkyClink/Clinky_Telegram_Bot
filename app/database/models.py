import os
from dotenv import load_dotenv


from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import (AsyncAttrs, async_sessionmaker,
                                    create_async_engine)


load_dotenv()
engine = create_async_engine(url=os.getenv('SQLALCHEMY_URL'))


async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25))
    documentation: Mapped[str] = mapped_column(String(255), server_default='No documentation')
    items = relationship('Item', back_populates='category')


class Object(Base):
    __tablename__ = 'objects'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25))
    items = relationship('Item', back_populates='object')


class Item(Base):
    __tablename__ = 'items'

    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[str] = mapped_column(String(10))
    description: Mapped[str] = mapped_column(String(120))
    amperage: Mapped[int] = mapped_column()
    current_amperage: Mapped[int] = mapped_column(server_default='-1')
    status: Mapped[str] = mapped_column(String(30), default='No data', server_default='No data')
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    category = relationship('Category', back_populates='items')
    object_id: Mapped[int] = mapped_column(ForeignKey('objects.id'))
    object = relationship('Object', back_populates='items')


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
