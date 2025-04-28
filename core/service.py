import asyncio
import threading
from services.background_service import background_worker

class BackgroundService:
    def __init__(self):
        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=self.start)

    def start(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(background_worker())

    def run(self):
        self.thread.start()
