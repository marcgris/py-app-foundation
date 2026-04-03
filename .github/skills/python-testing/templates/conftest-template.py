# templates/conftest-template.py
# Place at tests/conftest.py
# Adjust DB URL and app imports to match your project

from __future__ import annotations

import asyncio

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from src.db.base import Base
from src.dependencies import get_session
from src.main import app

# ── Event Loop ──────────────────────────────────────────────────────────────


@pytest.fixture(scope="session")
def event_loop():
    """Single event loop for the entire test session."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


# ── Database ─────────────────────────────────────────────────────────────────

TEST_DATABASE_URL = "postgresql+asyncpg://test:test@localhost:5432/test_db"


@pytest.fixture(scope="session")
async def engine():
    """Create the test database schema once per session."""
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture
async def db_session(engine) -> AsyncSession:
    """
    Each test gets a session that is rolled back after the test.
    This keeps tests isolated without wiping the schema.
    """
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        async with session.begin():
            yield session
            await session.rollback()


# ── HTTP Client ───────────────────────────────────────────────────────────────


@pytest.fixture
async def client(db_session: AsyncSession) -> AsyncClient:
    """
    HTTPX client wired to the test DB session.
    Overrides the FastAPI get_session dependency.
    """

    async def override_session():
        yield db_session

    app.dependency_overrides[get_session] = override_session
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as c:
        yield c
    app.dependency_overrides.clear()


# ── Data Factories ────────────────────────────────────────────────────────────


@pytest.fixture
def make_user(db_session: AsyncSession):
    """Factory fixture for creating test users with sensible defaults."""
    from src.models.user import UserCreate
    from src.repositories.user import SQLAlchemyUserRepository

    repo = SQLAlchemyUserRepository(db_session)

    async def _make(
        email: str = "test@example.com",
        name: str = "Test User",
        **kwargs,
    ):
        return await repo.create(UserCreate(email=email, name=name, **kwargs))

    return _make
