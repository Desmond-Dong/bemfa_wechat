import aiohttp
import asyncio

class OpenWrtConnection:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        self.token = None

    async def connect(self):
        async with aiohttp.ClientSession() as session:
            payload = {
                'method': 'login',
                'params': [self.username, self.password],
                'id': 1,
                'jsonrpc': '2.0'
            }
            async with session.post(f'http://{self.host}/cgi-bin/luci/rpc/auth', json=payload) as response:
                result = await response.json()
                if 'result' in result:
                    self.token = result['result']
                    return self.token
                else:
                    raise Exception("Failed to connect to OpenWrt: " + str(result))

