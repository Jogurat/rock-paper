from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.settings import settings

engine = create_async_engine(
    f"postgresql+asyncpg://{settings().postgres_user}:{settings().postgres_password}@{settings().postgres_host}/{settings().postgres_db}",
    echo=True,
)
AsyncSessionLocal = async_sessionmaker(bind=engine)
