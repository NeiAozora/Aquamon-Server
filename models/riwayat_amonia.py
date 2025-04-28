from core.db import db
from datetime import datetime

class RiwayatAmonia(db.Model):
    __tablename__ = 'riwayat_amonia'

    id_riwayat = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_kolam = db.Column(db.Integer, db.ForeignKey('kolam.id_kolam'), nullable=False)
    kadar_amonia = db.Column(db.Float, nullable=False)
    waktu_pencatatan = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
