from contextlib import asynccontextmanager

from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

from app.database.session import create_db_and_tables

from .API.router import router


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    print("Starting up...")
    create_db_and_tables()
    yield
    print("Shutting down...")


app = FastAPI(lifespan=lifespan_handler)

app.include_router(router)


# Scalar API documentation route
@app.get("/scalar-api", include_in_schema=False)
def scalar_api():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )
