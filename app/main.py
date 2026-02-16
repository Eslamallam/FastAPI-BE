from contextlib import asynccontextmanager
import asyncio

from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

from app.database.session import create_db_and_tables

from .API.router import router


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    print("Starting up...")

    async def _create_db():
        try:
            await create_db_and_tables()
            print("Database tables ensured")
        except Exception as e:
            print(f"Database initialization failed: {e}")

    # run DB setup in background so the app can start even if DB is slow/unavailable
    asyncio.create_task(_create_db())

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
