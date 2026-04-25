from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.config import get_settings
from app.db.base import Base

settings = get_settings()

# Create the async engine (the actual wire to the database)
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False, # Set to True if you want to see SQL queries in the terminal (good for debugging)
    pool_pre_ping=True, # Checks if connection is alive before using it
)

# Create a factory that makes temporary workers (sessions)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# This is the dependency we will inject into FastAPI routes later
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise