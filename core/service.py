import asyncio
import threading
import queue
from services.check_amonia_service import check_amonia_worker

class BackgroundService:
    def __init__(self, comm_queue):
        self.loop = asyncio.new_event_loop()  # Create a new event loop for background thread
        self.comm_queue = comm_queue  # Queue to communicate with the main thread
        self.lock = threading.Lock()  # Lock to synchronize access to shared state
        self.shared_value = None  # Shared value that threads will access

    def start(self):
        """Start background worker in a new event loop."""
        try:
            asyncio.set_event_loop(self.loop)  # Set event loop for this thread
            self.loop.run_until_complete(check_amonia_worker())  # Run the background worker

            while True:
                msg = self.comm_queue.get()  # Get message from queue
                if msg == "get_value":
                    self._get_shared_value()
                elif msg == "set_value":
                    self._set_shared_value()
                elif msg == "exit":
                    break  # Exit the loop and stop the background thread
        except Exception as e:
            print(f"Error in background worker: {e}")

    def run(self):
        """Initialize background thread."""
        self.thread = threading.Thread(target=self.start, daemon=True)  # Start background worker as a daemon thread
        self.thread.start()

    def _get_shared_value(self):
        """Thread-safe retrieval of shared value."""
        with self.lock:
            self.comm_queue.put(self.shared_value)  # Send back shared value to queue

    def _set_shared_value(self):
        """Thread-safe setting of shared value."""
        new_value = self.comm_queue.get()  # Get new value from queue
        with self.lock:
            self.shared_value = new_value
        print(f"Background Service: Set shared value to {new_value}")

