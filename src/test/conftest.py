from collections.abc import AsyncGenerator
from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.core.config import settings
from src.db.base import Base, get_db_session
from src.main import app


class SettingsForTests(BaseSettings):
    TEST_DATABASE_URL: str

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[2] / ".env",
        case_sensitive=True,
        extra="ignore",
    )


test_settings = SettingsForTests()
test_database_url = make_url(test_settings.TEST_DATABASE_URL)
application_database_url = make_url(settings.DATABASE_URL)

if not test_database_url.database or "test" not in test_database_url.database.lower():
    raise ValueError("TEST_DATABASE_URL must target a database with 'test' in its name")
if test_database_url.database == application_database_url.database:
    raise ValueError("TEST_DATABASE_URL must be separate from DATABASE_URL")


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(scope="session")
async def test_engine() -> AsyncGenerator[AsyncEngine, None]:
    engine = create_async_engine(test_settings.TEST_DATABASE_URL, echo=False)
    schema_created = False
    try:
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)
        schema_created = True
        yield engine
    finally:
        try:
            if schema_created:
                async with engine.begin() as connection:
                    await connection.run_sync(Base.metadata.drop_all)
        finally:
            await engine.dispose()


@pytest.fixture
async def db_session(test_engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    async with test_engine.connect() as connection:
        transaction = await connection.begin()
        session_factory = async_sessionmaker(
            bind=connection,
            class_=AsyncSession,
            expire_on_commit=False,
            join_transaction_mode="create_savepoint",
        )
        try:
            async with session_factory() as session:
                yield session
        finally:
            if transaction.is_active:
                await transaction.rollback()


@pytest.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield db_session

    previous_override = app.dependency_overrides.get(get_db_session)
    app.dependency_overrides[get_db_session] = override_get_db
    try:
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
        ) as async_client:
            yield async_client
    finally:
        if previous_override is None:
            app.dependency_overrides.pop(get_db_session, None)
        else:
            app.dependency_overrides[get_db_session] = previous_override
