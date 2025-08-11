import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.dependencies import get_db
from app.database.models import Base, Player, Match

# Use SQLite for testing (supports UUIDs with proper handling)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture
async def test_db():
    # Create test engine
    engine = create_async_engine(TEST_DATABASE_URL)

    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Create session factory
    TestSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async def override_get_db():
        async with TestSessionLocal() as session:
            yield session

    # Override dependency
    app.dependency_overrides[get_db] = override_get_db

    yield TestSessionLocal

    # Cleanup
    app.dependency_overrides.clear()
    await engine.dispose()


@pytest_asyncio.fixture
async def client(test_db):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test", follow_redirects=True
    ) as ac:
        yield ac


@pytest_asyncio.fixture
async def sample_player(test_db):
    """Create a sample player for testing"""
    async with test_db() as session:
        player = Player(username="testplayer")
        session.add(player)
        await session.commit()
        await session.refresh(player)
        return player


@pytest_asyncio.fixture
async def sample_match(test_db):
    """Create a sample match for testing"""
    async with test_db() as session:
        match = Match()
        session.add(match)
        await session.commit()
        await session.refresh(match)
        return match
