from core.db import db

class Kolam(db.Model):
    __tablename__ = 'kolam'

    id_kolam = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id_user'), nullable=False)
    nama_kolam = db.Column(db.String(100), nullable=False)
    lokasi = db.Column(db.String(255))
    deskripsi = db.Column(db.Text)
    pengurasan_otomatis = db.Column(db.Boolean, default=True)
