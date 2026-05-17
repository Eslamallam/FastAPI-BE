import datetime
from enum import Enum
from pydantic import EmailStr
from sqlmodel import SQLModel, Field

class ShipmentStatus(str, Enum):
    delivered = "Delivered"
    in_transit = "In Transit"
    processing = "Processing"

class Shipment(SQLModel, table=True):
    __tablename__ = "shipment"

    id: int = Field(default=None, primary_key=True)
    content: str
    destination: str
    weight: float = Field(gt=0, le=250)  # weight in kg
    status: ShipmentStatus
    estimated_delivery: datetime.datetime

class Seller(SQLModel, table=True):
    __tablename__ = "seller"

    id: int = Field(default=None, primary_key=True)
    name: str
    email: EmailStr
    password_hash: str