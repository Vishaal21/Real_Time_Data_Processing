from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER

# Use asyncpg driver and create_async_engine
engine = create_async_engine(
    f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Create async sessionmaker
SessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,  # Ensure the session class is AsyncSession
)


# Async generator for database sessions
async def get_db():
    try:
        async with SessionLocal() as db:
            yield db
    finally:
        await db.close()


from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Define the database URL (change this as per your DB config)
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create a synchronous engine
engine = create_engine(DATABASE_URL)

# Create a session factory for synchronous sessions
SessionLocalSync = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Function to get a database session
@contextmanager  # convert my fxn into generator based context manager
def get_sync_db():  # it returns a generator object that is designed to be used with a with(caller) statement.
    with SessionLocalSync() as db:
        try:
            yield db  # Provide the session to the caller
        finally:
            db.close()  # Ensure the session is closed after use
