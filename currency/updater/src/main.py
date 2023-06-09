import asyncio
import datetime as dt
import time

import aiohttp
import redis.asyncio as aioredis
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from scheduler.asyncio import Scheduler

from src.app.application import UpdaterCurrencyApplication
from src.config import get_redis_config, get_mongo_config


async def foo():
    pass


async def main():
    mongo_config = get_mongo_config()
    redis_config = get_redis_config()
    client = AsyncIOMotorClient(mongo_config.uri)
    db: AsyncIOMotorDatabase = client.get_database(mongo_config.db)

    redis = aioredis.Redis(
        host=redis_config.host, port=redis_config.port, db=redis_config.db
    )
    session = aiohttp.ClientSession()

    app = UpdaterCurrencyApplication(db, redis, session)

    service_for_run = app.build()

    async def run() -> None:
        await service_for_run.update_currencies()
        return

    await run()
    while True:
        await asyncio.sleep(10000)
        await run()


if __name__ == "__main__":
    asyncio.run(main())
