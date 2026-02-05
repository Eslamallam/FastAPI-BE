from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from typing import Any

from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference

from app.database.models import Shipment, ShipmentStatus
from app.database.session import SessionDep, create_db_and_tables

from .schemas import ShipmentCreate, ShipmentRead, ShipmentUpdate


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    print("Starting up...")
    create_db_and_tables()
    yield
    print("Shutting down...")


app = FastAPI(lifespan=lifespan_handler)

@app.get("/shipment/latest")
def get_latest_shipment(session: SessionDep) -> dict[str, Any]:
    from sqlmodel import select
    statement = select(Shipment).order_by(Shipment.id.desc()).limit(1)
    latest_shipment = session.exec(statement).first()
    if not latest_shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No shipments found"
        )
    return {"id": latest_shipment.id, "details": latest_shipment}


@app.get("/shipment")
def get_shipment(id: int, session: SessionDep) -> ShipmentRead:
    shipment = session.get(Shipment, id)
    if not shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found"
        )
    return shipment


@app.post("/shipment")
def create_shipment(body: ShipmentCreate, session: SessionDep) -> dict[str, Any]:
    new_shipment = Shipment(
        content=body.content,
        status=ShipmentStatus.processing,
        weight=body.weight,
        destination=body.destination,
        estimated_delivery=datetime.now() + timedelta(days=3)
    )
    session.add(new_shipment)
    session.commit()
    session.refresh(new_shipment)
    return {"id": new_shipment.id, "details": new_shipment}


@app.put("/shipment")
def update_shipment(id: int, body: ShipmentUpdate, session: SessionDep) -> dict[str, Any]:
    shipment = session.get(Shipment, id)
    if not shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found"
        )

    shipment.sqlmodel_update(body.model_dump(exclude_none=True))
    session.add(shipment)
    session.commit()
    session.refresh(shipment)

    return {"id": id, "details": shipment}


@app.patch("/shipment")
def patch_shipment(id: int, body: ShipmentUpdate, session: SessionDep) -> dict[str, Any]:
    shipment = session.get(Shipment, id)
    if not shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found"
        )
    shipment.sqlmodel_update(body.model_dump(exclude_none=True))
    session.add(shipment)
    session.commit()
    session.refresh(shipment)
    return {"id": id, "details": shipment}


@app.delete("/shipment")
def delete_shipment(id: int, session: SessionDep) -> dict[str, Any]:
    shipment = session.get(Shipment, id)
    if not shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found"
        )

    deleted_shipment = shipment
    session.delete(shipment)
    session.commit()
    return {"id": id, "details": deleted_shipment}


# Scalar API documentation route
@app.get("/scalar-api", include_in_schema=False)
def scalar_api():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )
