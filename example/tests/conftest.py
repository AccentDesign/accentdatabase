# isort: off
from os import environ

environ.setdefault(
    "DATABASE_URL", "postgresql+asyncpg://postgres:password@localhost:5433/testdb"
)

import asyncio
import contextlib

import pytest
import pytest_asyncio
from accentdatabase.base import Base
from accentdatabase.config import config
from accentdatabase.engine import engine
from accentdatabase.session import get_session
from accentdatabase.testing import recreate_postgres_database
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from main import app, Item


@pytest.fixture(scope="session")
def event_loop(request):
    """pytest fixture to create an event loop"""

    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(name="db_setup", scope="session", autouse=True)
async def db_setup_fixture():
    await recreate_postgres_database(config.url)


@pytest_asyncio.fixture(name="db_migrations", scope="session", autouse=True)
async def db_migrations_fixture(db_setup):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    # dispose the engine
    await engine.dispose()


@pytest_asyncio.fixture(name="db_initial_data")
async def db_initial_data_fixture(db_migrations):
    get_db_session = contextlib.asynccontextmanager(get_session)
    async with get_db_session() as session:
        instance = Item(name="steve")
        session.add(instance)
        await session.commit()


@pytest_asyncio.fixture(name="db_session")
async def db_session_fixture():
    """create a sqlalchemy session"""

    # create a sqlalchemy connection
    connection = await engine.connect()
    # begin a new database transaction
    trans = await connection.begin()
    # create a sessionmaker
    async_session = sessionmaker(
        engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )
    # create a new session and bind it to the connection
    # this will ensure that when the transaction is rolled back
    # all calls to the session's commit will be rolled back as well
    async with async_session(bind=connection) as session:
        yield session

    # rollback the transaction
    await trans.rollback()
    # close the connection
    await connection.close()


@pytest_asyncio.fixture(name="client")
async def client_fixture(db_session: AsyncSession):
    """the client to use in the tests"""

    # override the database session for the app
    # this is to ensure that the database session is always the same
    # as the one used in the tests so that the session commits are
    # always rolled back in the session fixture above
    app.dependency_overrides[get_session] = lambda: db_session
    # create a client
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
    # restore the original database session
    app.dependency_overrides.clear()
