import asyncio

from notes_sync.broker import Consumer
from notes_sync.logger import Logger


async def main():
    async with Consumer.get("health_check") as consumer:
        for message in consumer:
            Logger.debug("Got health_check message")


if __name__ == "__main__":
    asyncio.run(main())
