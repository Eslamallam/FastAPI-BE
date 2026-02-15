from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class ShipmentStatus(str, Enum):
    delivered = "Delivered"
    in_transit = "In Transit"
    processing = "Processing"


class BaseShipment(BaseModel):
    content: str = Field(min_length=3, max_length=100)
    status: ShipmentStatus = Field(default=ShipmentStatus.processing)
    weight: float = Field(description="Weight in kilograms (kgs)", gt=0, le=25)
    destination: str = Field(min_length=3, max_length=100, default="Unknown")


class ShipmentRead(BaseShipment):
    status: ShipmentStatus
    estimated_delivery: datetime


class ShipmentCreate(BaseShipment):
    pass


class ShipmentUpdate(BaseModel):
    content: str = Field(min_length=3, max_length=100)
    status: ShipmentStatus | None = Field(default=None)
    estimated_delivery: datetime | None = Field(default=None)
