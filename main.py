from core.server import Server
from core.service import BackgroundService
from config import HOST_DEVELOPMENT
import sys
import threading
import time
import traceback

sys.dont_write_bytecode = True

def run_background_service():
    try:
        background_service = BackgroundService()
        background_service.run()
    except Exception:
        print("[BackgroundService] Crashed. Retrying once...")
        traceback.print_exc()
        try:
            background_service = BackgroundService()
            background_service.run()
        except Exception:
            print("[BackgroundService] Failed again. Giving up.")
            traceback.print_exc()


if __name__ == "__main__":
    # Jalankan background service di thread terpisah dengan restart logic
    background_service_thread = threading.Thread(target=run_background_service, daemon=True)
    background_service_thread.start()

    try:
        # Jalankan Flask server di thread utama
        server = Server()
        server.run(host=HOST_DEVELOPMENT, debug=True)
    except KeyboardInterrupt:
        print("Shutting down gracefully...")
        sys.exit(0)
    except Exception as e:
        print("[Server] Crashed with exception:")
        traceback.print_exc()
        sys.exit(1)
