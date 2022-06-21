from aiohttp import ClientSession
from prozorro_crawler.main import main
from .db import upsert_tenders


async def data_handler(_: ClientSession, items: list):
    await upsert_tenders(items)


if __name__ == "__main__":
    main(data_handler)
