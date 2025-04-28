from core.db import db
from datetime import datetime

class DeviceStatus(db.Model):
    __tablename__ = 'device_status'

    id_status = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_kolam = db.Column(db.Integer, db.ForeignKey('kolam.id_kolam'), nullable=False)
    status_online = db.Column(db.Boolean, nullable=False)
    terakhir_update = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
