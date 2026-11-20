from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.settings import settings

engine = create_async_engine(
    url=settings.DATABASE_URL,
    pool_size=5,
    max_overflow=10,
)

session_factory = async_sessionmaker(engine, class_=AsyncSession)

async def get_async_session():
    async with session_factory() as session:
        yield session
