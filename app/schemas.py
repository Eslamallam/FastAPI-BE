from pydantic import BaseModel, Field


class Shipment(BaseModel):
    content: str = Field(min_length=3, max_length=100)
    status: str
    weight: float = Field(description="Weight in kilograms (kgs)", gt=0, le=25)
