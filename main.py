import sys
import threading
import asyncio

from core.server import Server
from core.logger import logger
from config import HOST_DEVELOPMENT
from services.check_amonia_service import AmoniaChecker


def start_background_loop(loop, amonia_checker):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(amonia_checker.run())

async def run_server(server):
    server.run(host=HOST_DEVELOPMENT, debug=True)

if __name__ == "__main__":
    try:
        server = Server()

        # Jalankan background task di thread terpisah
        background_loop = asyncio.new_event_loop()
        amonia_checker = AmoniaChecker(server.app)

        background_thread = threading.Thread(
            target=start_background_loop,
            args=(background_loop, amonia_checker),
            daemon=True
        )
        background_thread.start()

        # Jalankan server di thread utama
        asyncio.run(run_server(server))

    except KeyboardInterrupt:
        print("Shutting down gracefully...")
        sys.exit(0)
