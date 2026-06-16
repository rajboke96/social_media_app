# from sqlalchemy import URL, create_engine
# from sqlalchemy.orm import sessionmaker


# url_object=URL.create(
#     drivername="mysql+mysqlconnector",
#     username="root",
#     password="mysqlD123",  # No manual escaping needed here
#     host="localhost",
#     database="social_media_app"
# )
# engine = create_engine(url_object)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# def get_db():
#     db = SessionLocal()
#     try: yield db
#     finally: 
#         print("closing db connection!")
#         db.close()

from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import select

# 1. Database Configuration (Note the mysql+aiomysql:// protocol)
DATABASE_URL = "mysql+aiomysql://root:mysqlD123@localhost:3306/social_media_app"

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
    return AsyncSessionLocal