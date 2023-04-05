from aiohttp import ClientSession
from aiohttp import TCPConnector


# should return a session
async def create_session():
    return ClientSession(connector=TCPConnector(verify_ssl=False))