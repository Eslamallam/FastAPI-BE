from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, Session

from .config import settings

engine = create_async_engine(url=settings.POSTGRES_SERVER, echo=True)

# create the database and tables
async def create_db_and_tables():
    async with engine.begin() as conn:
        from .models import Shipment

        await conn.run_sync(SQLModel.metadata.create_all)


# session to be used in the endpoints
async def get_session():

    session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with session_maker(engine) as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]
