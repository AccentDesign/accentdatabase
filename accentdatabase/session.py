from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from accentdatabase.engine import engine


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
