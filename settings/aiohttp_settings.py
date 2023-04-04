from aiohttp import ClientSession
from aiohttp import TCPConnector


async def create_session():
    return ClientSession(connector=TCPConnector(verify_ssl=False))