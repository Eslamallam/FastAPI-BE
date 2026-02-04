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

class ShipmentRead(BaseShipment):
    status: ShipmentStatus

class ShipmentCreate(BaseShipment):
    pass

class ShipmentUpdate(BaseModel):
    content: str = Field(min_length=3, max_length=100)
    status: ShipmentStatus

