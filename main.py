from core.server import Server
from core.service import BackgroundService
from config import HOST_DEVELOPMENT
import sys
sys.dont_write_bytecode = True


if __name__ == "__main__":
    
    server = Server()
    background_service = BackgroundService()

    background_service.run()
    
    server.setup()
    server.run(host=HOST_DEVELOPMENT, debug=True)
