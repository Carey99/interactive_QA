"""
Test script for API endpoints
"""
import asyncio
import aiohttp

async def test_health():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://localhost:8001/health') as resp:
            print(f"Health check: {resp.status}")

if __name__ == "__main__":
    asyncio.run(test_health())
