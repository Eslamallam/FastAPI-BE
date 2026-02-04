from enum import Enum
from sqlmodel import SQLModel, Field

class ShipmentStatus(str, Enum):
    delivered = "Delivered"
    in_transit = "In Transit"
    processing = "Processing"

class Shipment(SQLModel):
    id: int = Field(default=None, primary_key=True)
    content: str
    destination: str
    weight: float = Field(gt=0, le=250)  # weight in kg
    status: ShipmentStatus
    estimated_delivery: str