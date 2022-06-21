import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import PyMongoError
from pymongo.operations import ReplaceOne
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
            except PyMongoError as e:
                logger.warning({"message": "Retry on mongo error",
                                "error": e, "error_args": e.args},
                               extra={"MESSAGE_ID": "MONGODB_EXCEPTION"})
                await asyncio.sleep(ERROR_INTERVAL)
    return decorated


__collection = None


def get_collection():
    global __collection
    print(["get_collection", __collection])
    if __collection is None:
        client = AsyncIOMotorClient(MONGODB_URL)
        __collection = client[MONGODB_DATABASE][MONGODB_COLLECTION]
    return __collection


@retry_decorator
async def upsert_tenders(tenders: list):
    operations = []
    for t in tenders:
        uid = t.pop("id")
        operations.append(ReplaceOne({"_id": uid}, t, upsert=True))
    result = await get_collection().bulk_write(operations)
    print([result.inserted_count, result.modified_count])

