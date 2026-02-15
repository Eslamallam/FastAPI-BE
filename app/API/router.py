import datetime
from typing import Any
from fastapi import APIRouter, HTTPException, status

from app.database.models import Shipment
from app.database.session import SessionDep
from app.API.schemas.shipment import ShipmentCreate, ShipmentRead, ShipmentUpdate
from app.services.shipment import ShipmentService

router = APIRouter()


@router.get("/shipment")
async def get_shipment(id: int, session: SessionDep) -> ShipmentRead:
    shipment = ShipmentService(session).get_shipment(id)
    if not shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found"
        )
    return shipment


@router.post("/shipment")
async def create_shipment(body: ShipmentCreate, session: SessionDep) -> dict[str, Any]:
    new_shipment = await ShipmentService(session).create_shipment(body)
    return {"id": new_shipment.id, "details": new_shipment}


@router.put("/shipment")
async def update_shipment(
    id: int, body: ShipmentUpdate, session: SessionDep
) -> dict[str, Any]:
    shipment = await session.get(Shipment, id)
    if not shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found"
        )

    shipment.sqlmodel_update(body.model_dump(exclude_none=True))
    session.add(shipment)
    await session.commit()
    await session.refresh(shipment)

    return {"id": id, "details": shipment}


@router.patch("/shipment")
async def patch_shipment(
    id: int, body: ShipmentUpdate, session: SessionDep
) -> dict[str, Any]:
    shipment = body.model_dump(exclude_none=True)
    if not shipment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update"
        )

    await ShipmentService(session).update_shipment(id, body)
    return {"id": id, "details": shipment}


@router.delete("/shipment")
async def delete_shipment(id: int, session: SessionDep) -> dict[str, Any]:
    await ShipmentService(session).delete_shipment(id)

    return {"id": f"Shipment with #{id} has been deleted"}
