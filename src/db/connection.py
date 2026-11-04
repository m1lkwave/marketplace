from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from src.settings import settings

engine = create_async_engine(
    url=settings.DATABASE_URL,
)

session_factory = async_sessionmaker(engine, class_=AsyncSession)

async def get_async_session():
    async with session_factory() as session:
        yield session
