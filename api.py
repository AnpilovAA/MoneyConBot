from aiohttp import ClientSession
import asyncio


async def main():
    async with ClientSession() as session:
        async with session.get(URL) as response:
            print(response.status)
            print(await response.text())


if __name__ == '__main__':
    asyncio.run(main())
