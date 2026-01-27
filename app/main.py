from fastapi import FastAPI, status, HTTPException
from scalar_fastapi import get_scalar_api_reference

from typing import Any

app = FastAPI()

db = {
    201: {
        "content": "Laptop",
        "status": "Delivered",
    },
    202: {
        "content": "Office Chair",
        "status": "In Transit",
    },
    203: {
        "content": "Monitor",
        "status": "Delivered",
    },
    204: {
        "content": "Keyboard",
        "status": "Processing",
    },
    205: {
        "content": "Mouse",
        "status": "Delivered",
    },
    206: {
        "content": "Desk Lamp",
        "status": "In Transit",
    },
    207: {
        "content": "Bookshelf",
        "status": "Processing",
    },
}


@app.get("/shipment/latest")
def get_latest_shipment() -> dict[str, Any]:
    latest_id = max(db.keys())
    return {"id": latest_id, "details": db[latest_id]}


@app.get("/shipment")
def get_shipment(id: int | None = None) -> dict[str, Any]:
    if id not in db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found"
        )

    return {"id": id, "details": db[id]}


@app.post("/shipment")
def create_shipment(content: str) -> dict[str, Any]:
    new_id = max(db.keys()) + 1
    db[new_id] = {"content": content, "status": "Processing"}
    return {"id": new_id, "details": db[new_id]}


@app.put("/shipment")
def update_shipment(id: int, content: str, status: str) -> dict[str, Any]:
    if id not in db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found"
        )

    db[id] = {
        "content": content,
        "status": status,
    }

    return {"id": id, "details": db[id]}


@app.patch("/shipment")
def patch_shipment(id: int, body: dict[str, Any]) -> dict[str, Any]:
    if id not in db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found"
        )

    shipment = db[id]

    # if content is not None:
    #     shipment["content"] = content
    # if status is not None:
    #     shipment["status"] = status

    shipment.update(body)

    db[id] = shipment
    return {"id": id, "details": shipment}


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
