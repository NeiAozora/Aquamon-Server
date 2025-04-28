import asyncio

async def background_worker():
    while True:
        print("🔄 Service background jalan terus...")
        await asyncio.sleep(5)
