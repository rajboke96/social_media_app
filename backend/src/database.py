
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
import os
from pathlib import Path
from src.logger import get_logger
logger = get_logger(__name__)

DB_ROOT_PASSWORD=os.environ["DB_ROOT_PASSWORD"]
DB_PORT=os.environ["DB_PORT"]
DB_NAME=os.environ["DB_NAME"]
# 1. Database Configuration (Note the mysql+aiomysql:// protocol)
DATABASE_URL = f"mysql+aiomysql://root:{DB_ROOT_PASSWORD}@db:{DB_PORT}/{DB_NAME}"
UPLOAD_DIR = os.environ["UPLOAD_DIR"]

# 2. Create the Async Engine (Global Connection Pool)
# pool_pre_ping checks if the connection is alive before using it
engine = create_async_engine(
    DATABASE_URL,
    pool_recycle=1800,  # Recycles connections every 30 minutes
    echo=False
    # pool_pre_ping=True  <--- DELETE OR REMOVE THIS LINE ENTIRELY
)

# 3. Create the Async Session Factory
# expire_on_commit=False prevents SQLAlchemy from breaking models after a commit
AsyncSessionLocal = async_sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# 6. Per-Request Lifespan Dependency (Yield Pattern)
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

# Instead of passing a finished live session instance down the context wire...
async def get_db_factory():
    logger.info('exit')
    return AsyncSessionLocal
