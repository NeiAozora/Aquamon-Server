import asyncio
from helpers.create_riwayat import create_riwayat


async def background_worker():
    while True:
        print("🔄 Service background berjalan...")
        await asyncio.sleep(5)
