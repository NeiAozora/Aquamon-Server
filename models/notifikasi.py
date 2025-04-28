from core.db import db
from datetime import datetime

class Notifikasi(db.Model):
    __tablename__ = 'notifikasi'

    id_notifikasi = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_kolam = db.Column(db.Integer, db.ForeignKey('kolam.id_kolam'), nullable=False)
    judul = db.Column(db.String(100), nullable=False)
    pesan = db.Column(db.Text, nullable=False)
    dibaca = db.Column(db.Boolean, default=False)
    waktu_dibuat = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
