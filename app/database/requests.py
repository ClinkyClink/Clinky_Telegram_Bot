from app.database.models import User, Item, Object, async_session

from sqlalchemy import select
from sqlalchemy.orm import joinedload


async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalars(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()


async def get_objects():
    async with async_session() as session:
        return await session.scalars(select(Object))


async def get_item_by_object(object_id):
    async with async_session() as session:
        return await session.scalars(select(Item).where(
            Item.object_id == object_id)
        )


async def get_item(item_id):
    async with async_session() as session:
        result = await session.execute(
            select(Item).options(joinedload(Item.category)).where(
                Item.id == item_id
            )
        )
        return result.scalars().first()
