import sys
from typing import AsyncGenerator
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from osiris import settings

db_connection_str = settings.db_async_connection_str
if "pytest" in sys.modules:
    db_connection_str = settings.db_async_test_connection_str


BaseDB = declarative_base()

async_engine = create_async_engine(
    db_connection_str,
    echo=True,
    future=True
)

async_session = sessionmaker(
    async_engine, class_ = AsyncSession, expire_on_commit=False
)

# Dependency
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

async def init_models() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(BaseDB.metadata.drop_all)
        await conn.run_sync(BaseDB.metadata.create_all)
    print("Reinint models done")