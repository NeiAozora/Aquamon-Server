from flask import Flask
from config import Config
from core.db import db
from routes.route import register_routes

from models.user import User
from models.device_status import DeviceStatus
from models.kolam import Kolam
from models.notifikasi import Notifikasi
from models.riwayat_amonia import RiwayatAmonia
from models.riwayat_pengurasan import RiwayatPengurasan
from models.user_settings import UserSettings

# Module-level variable to hold the Server instance
global_server = None

def set_global_server(server_instance):
    """
    Set the global server instance so that other threads can import it.
    """
    global global_server
    global_server = server_instance


def get_global_server():
    """
    Get the global server instance.
    """
    return global_server

class Server:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config.from_object(Config)

        db.init_app(self.app)
        self._setup()

    def _setup(self):
        with self.app.app_context():
            register_routes(self.app)

            models = [
                User,
                UserSettings,
                Kolam,
                Notifikasi,
                DeviceStatus,
                RiwayatAmonia,
                RiwayatPengurasan
            ]

            for model in models:
                model.__table__.create(db.engine, checkfirst=True)

    def get_flask_instance(self):
        return self.app

    def run(self, **kwargs):
        self.app.run(**kwargs)


