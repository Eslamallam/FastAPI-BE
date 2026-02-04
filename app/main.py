from fastapi import FastAPI, status, HTTPException
from scalar_fastapi import get_scalar_api_reference

from typing import Any
from .schemas import ShipmentRead, ShipmentCreate, ShipmentUpdate

app = FastAPI()

db = {
    201: {
        "content": "Laptop",
        "status": "Delivered",
        "weight": 2.1,
    },
    202: {
        "content": "Office Chair",
        "status": "In Transit",
        "weight": 15.3,
    },
    203: {
        "content": "Monitor",
        "status": "Delivered",
        "weight": 4.7,
    },
    204: {
        "content": "Keyboard",
        "status": "Processing",
        "weight": 0.8,
    },
    205: {
        "content": "Mouse",
        "status": "Delivered",
        "weight": 0.3,
    },
    206: {
        "content": "Desk Lamp",
        "status": "In Transit",
        "weight": 1.2,
    },
    207: {
        "content": "Bookshelf",
        "status": "Processing",
        "weight": 22.5,
    },
}


@app.get("/shipment/latest")
def get_latest_shipment() -> dict[str, Any]:
    latest_id = max(db.keys())
    return {"id": latest_id, "details": db[latest_id]}


@app.get("/shipment")
def get_shipment(id: int) -> ShipmentRead:
    if id not in db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found"
        )

    #shipment = db[id]
    return db[id]


@app.post("/shipment")
def create_shipment(body: ShipmentCreate) -> dict[str, Any]:
    new_id = max(db.keys()) + 1
    db[new_id] = {"content": body.content, "status": "Processing", "weight": body.weight}
    return {"id": new_id, "details": db[new_id]}


@app.put("/shipment")
def update_shipment(id: int, body: ShipmentUpdate) -> dict[str, Any]:
    if id not in db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found"
        )

    db[id] = {
        "content": body.content,
        "status": body.status,
    }

    return {"id": id, "details": db[id]}


@app.patch("/shipment")
def patch_shipment(id: int, body: ShipmentUpdate) -> dict[str, Any]:
    if id not in db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found"
        )
    db[id].update(body.model_dump(exclude_unset=True))
    return db[id]


@app.delete("/shipment")
def delete_shipment(id: int) -> dict[str, Any]:
    if id not in db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found"
        )

    deleted_shipment = db.pop(id)
    return {"id": id, "details": deleted_shipment}


# Scalar API documentation route
@app.get("/scalar-api", include_in_schema=False)
def scalar_api():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )
