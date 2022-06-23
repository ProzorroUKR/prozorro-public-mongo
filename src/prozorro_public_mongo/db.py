import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Callable
from prozorro_public_mongo.settings import (
    MONGODB_COLLECTION,
    MONGODB_DATABASE,
    MONGODB_URL,
    ERROR_INTERVAL,
)
from logging import getLogger

logger = getLogger(__name__)


def retry_decorator(func: Callable) -> Callable:
    async def decorated(*args, **kwargs):
        while True:
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                logger.warning({"message": "Retry on error",
                                "error": e, "error_args": e.args},
                               extra={"MESSAGE_ID": "RETRY_EXCEPTION"})
                await asyncio.sleep(ERROR_INTERVAL)
    return decorated


__collection = None


def get_collection():
    global __collection
    if __collection is None:
        client = AsyncIOMotorClient(MONGODB_URL)
        __collection = client[MONGODB_DATABASE][MONGODB_COLLECTION]
    return __collection


@retry_decorator
async def upsert_tender(uid: str, data: dict):
    await get_collection().replace_one({"_id": uid}, data, upsert=True)

