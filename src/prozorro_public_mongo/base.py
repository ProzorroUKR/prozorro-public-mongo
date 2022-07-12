from prozorro_crawler.settings import BASE_URL, API_RESOURCE
from .db import retry_decorator, upsert_object
from contextlib import asynccontextmanager


@retry_decorator
async def get_object(session, uid):
    response = await session.get(f"{BASE_URL}/{API_RESOURCE}/{uid}")
    if response.status != 200:
        raise AssertionError(await response.text())
    result = await response.json()
    return result["data"]


@asynccontextmanager
async def get_and_save_object(session, uid):
    data = await get_object(session, uid)
    yield data
    await upsert_object(uid, data)
