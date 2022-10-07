from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from accentdatabase.engine import engine


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    returns an async session object.

    - example FastAPI usage::

        from accentdatabase.session import get_session
        from fastapi import Depends, FastApi
        from sqlalchemy import select
        from sqlalchemy.ext.asyncio import AsyncSession

        app = FastAPI()

        @app.get("/items")
        async def items(session: AsyncSession = Depends(get_session)):
            qs = select(Item)
            return (await session.execute(qs)).scalars().all()

    """

    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
