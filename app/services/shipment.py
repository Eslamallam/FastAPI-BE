import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.API.schemas.shipment import ShipmentCreate, ShipmentStatus, ShipmentUpdate
from app.database.models import Shipment


class ShipmentService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_shipment(self, id: int) -> Shipment:
        shipment = await self.session.get(Shipment, id)
        if not shipment:
            raise Exception("Shipment not found")
        return shipment

    async def create_shipment(self, shipment_data: ShipmentCreate) -> Shipment:
        new_shipment = Shipment(
            **shipment_data.model_dump(),
            status=ShipmentStatus.processing,
            estimated_delivery=datetime.now() + datetime.timedelta(days=3),
        )
        self.session.add(new_shipment)
        await self.session.commit()
        await self.session.refresh(new_shipment)
        return new_shipment

    async def update_shipment(self, id: int, shipment_data: ShipmentUpdate) -> Shipment:
        shipment = await self.get_shipment(id)
        shipment.sqlmodel_update(shipment_data.model_dump(exclude_none=True))
        self.session.add(shipment)
        await self.session.commit()
        await self.session.refresh(shipment)
        return shipment

    async def delete_shipment(self, id: int) -> None:
        shipment = await self.get_shipment(id)
        await self.session.delete(shipment)
        await self.session.commit()
