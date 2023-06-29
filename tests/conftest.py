from typing import AsyncGenerator

import pytest
import asyncio

from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from fastapi.testclient import TestClient
from httpx import AsyncClient

from src.config import DB_USER_TEST, DB_PASS_TEST, DB_HOST_TEST, DB_PORT_TEST, DB_NAME_TEST
from database import get_async_session
from src.main import app

from src.station.models import metadata

DATABASE_URL_TEST = f"postgresql+asyncpg://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}"


class Base(DeclarativeBase):
    pass


engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session_maker = async_sessionmaker(engine_test, expire_on_commit=False)
metadata.bind = engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.drop_all)


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


client = TestClient(app)


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
