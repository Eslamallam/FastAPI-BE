from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session

DATABASE_URL = "sqlite:///app.db"

engine = create_engine(
    DATABASE_URL, echo=True, connect_args={"check_same_thread": False}
)



def create_db_and_tables():
    from .models import Shipment
    SQLModel.metadata.create_all(bind=engine)


def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]