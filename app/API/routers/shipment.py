from typing import Any
from fastapi import APIRouter, HTTPException, status

from ..dependencies import ServiceDep
from database.models import Shipment
from ..schemas.shipment import ShipmentCreate, ShipmentRead, ShipmentUpdate

router = APIRouter(prefix="/api/v1/shipment", tags=["Shipment"])


@router.get("/")
async def get_shipment(id: int, service: ServiceDep) -> ShipmentRead:
    shipment = await service.get_shipment(id)
    if not shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found"
        )
    return shipment


@router.post("/")
async def create_shipment(body: ShipmentCreate, service: ServiceDep) -> dict[str, Any]:
    new_shipment = await service.create_shipment(body)
    return {"id": new_shipment.id, "details": new_shipment}


@router.put("/")
async def update_shipment(
    id: int, body: ShipmentUpdate, service: ServiceDep
) -> dict[str, Any]:
    shipment = await service.get(Shipment, id)
    if not shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found"
        )

    shipment.sqlmodel_update(body.model_dump(exclude_none=True))
    service.add(shipment)
    await service.commit()
    await service.refresh(shipment)

    return {"id": id, "details": shipment}


@router.patch("/")
async def patch_shipment(
    id: int, body: ShipmentUpdate, service: ServiceDep
) -> dict[str, Any]:
    shipment = body.model_dump(exclude_none=True)
    if not shipment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update"
        )

    await service.update_shipment(id, body)
    return {"id": id, "details": shipment}


@router.delete("/shipment")
async def delete_shipment(id: int, service: ServiceDep) -> dict[str, Any]:
    await service.delete_shipment(id)

    return {"id": f"Shipment with #{id} has been deleted"}
