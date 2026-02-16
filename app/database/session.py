from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from .config import settings
from urllib.parse import quote_plus

# Build a proper SQLAlchemy URL for asyncpg
_db_user = quote_plus(str(settings.POSTGRES_USER))
_db_pass = quote_plus(str(settings.POSTGRES_PASSWORD))
DATABASE_URL = (
    f"postgresql+asyncpg://{_db_user}:{_db_pass}"
    f"@{settings.POSTGRES_SERVER}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
)

engine = create_async_engine(DATABASE_URL, echo=True)


# create the database and tables
async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


# session to be used in the endpoints
session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_session():
    async with session_maker() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]
