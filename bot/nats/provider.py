import asyncio

from bot.config import get_settings
import nats


class Provider:
    def __init__(self):
        self.nc = None

    async def connect(self):
        self.nc = await nats.connect(get_settings().nats_uri)

    async def ping(self):
        pass

    async def close(self):
        await self.nc.close()


provider = Provider()
loop = asyncio.get_event_loop()
loop.run_until_complete(provider.connect())
