from app.database.models import Object, async_session

from sqlalchemy import select


async def get_object_name(object_id):
    async with async_session() as session:
        query = select(Object).filter(Object.id==object_id)
        result = await session.execute(query)
        object = result.scalar()
        return object.name