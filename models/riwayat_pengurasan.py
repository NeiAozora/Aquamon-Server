from core.db import db
from datetime import datetime

class RiwayatPengurasan(db.Model):
    __tablename__ = 'riwayat_pengurasan'

    id_pengurasan = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_kolam = db.Column(db.Integer, db.ForeignKey('kolam.id_kolam'), nullable=False)
    waktu_pengurasan = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    jenis = db.Column(db.Enum('otomatis', 'manual', name='jenis_pengurasan'), nullable=False)
