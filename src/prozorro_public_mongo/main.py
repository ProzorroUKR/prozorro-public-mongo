from aiohttp import ClientSession
from prozorro_crawler.main import main
from prozorro_crawler.settings import BASE_URL
from .db import upsert_tender, retry_decorator
import asyncio


@retry_decorator
async def get_tender(session, uid):
    response = await session.get(f"{BASE_URL}/tenders/{uid}")
    if response.status != 200:
        raise AssertionError(await response.text())
    result = await response.json()
    return result["data"]


async def process_tender(session, uid):
    data = await get_tender(session, uid)
    # TODO filter data here
    data.pop("documents", None)
    for key in data.keys():
        if 'documents' in data[key].keys():
            data[key].pop('documents')
    # data.pop("complaints", None)
    await upsert_tender(uid, data)


async def data_handler(session: ClientSession, items: list):
    await asyncio.gather(*(
        process_tender(session, e["id"])
        for e in items
    ))


if __name__ == "__main__":
    main(data_handler)
