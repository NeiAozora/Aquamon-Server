from flask import Flask
from config import Config
from core.db import db
from routes.route import register_routes

class Server:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config.from_object(Config)
        db.init_app(self.app)
        self._setup()

    def _setup(self):
        with self.app.app_context():
            from models import user, kolam, device_status
            db.create_all()
            register_routes(self.app)

    def run(self, **kwargs):
        self.app.run(**kwargs)
