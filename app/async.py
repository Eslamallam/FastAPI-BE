import asyncio
import time


async def endpoint(route: str) -> str:
    print(f"Endpoint '{route}' has been called.")

    # emulate database processing
    await asyncio.sleep(1)
    print(f"Endpoint '{route}' <<< response.")
    return route

async def server():
    test = (
        "GET /shipment/latest",
        "GET /shipment?id=1",
        "POST /shipment",
    )

    requests = [
        asyncio.create_task(endpoint(route)) for route in test
    ]

    done, pending = await asyncio.wait(requests)

    for task in done:
        print(f"Task result: {task.result()}")


# run server
asyncio.run(server())
