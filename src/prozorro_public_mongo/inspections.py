from aiohttp import ClientSession
from prozorro_crawler.main import main
from .base import get_and_save_object
from .processing import filter_out_documents
import asyncio


async def process_item(session, uid):
    async with get_and_save_object(session, uid) as data:
        # filter data here
        filter_out_documents(data)


async def data_handler(session: ClientSession, items: list):
    print(len(items))
    await asyncio.gather(*(
        process_item(session, e["id"])
        for e in items
    ))


if __name__ == "__main__":
    main(data_handler)
