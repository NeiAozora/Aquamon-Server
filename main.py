from core.server import Server
from core.service import BackgroundService
from core.logger import logger
from config import HOST_DEVELOPMENT
import sys
import threading
import queue

from core.global_state import SharedState  # Import the shared state

# Initialize shared state
shared_state = SharedState()

def run_background_service():
    comm_queue = queue.Queue()

    # Create and run the background service
    background_service = BackgroundService(comm_queue)
    background_service.run()

    # Example of setting a shared value
    comm_queue.put("set_value")  # Request to set shared value
    comm_queue.put(logger)  # The value to set


if __name__ == "__main__":
    try:
        # Start Flask server in the main thread
        server = Server()

        # Set the global server instance
        shared_state.set_global_server(server)

        # Running background service in a separate thread
        background_service_thread = threading.Thread(target=run_background_service, daemon=True)
        background_service_thread.start()

        # Running Flask app in the main thread
        server.run(host=HOST_DEVELOPMENT, debug=True)

    except KeyboardInterrupt:
        print("Shutting down gracefully...")
        sys.exit(0)
