from core.db import db

class UserSettings(db.Model):
    __tablename__ = 'user_settings'

    id_setting = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id_user'), nullable=False)
    batasan_amonia = db.Column(db.Float, default=0.25)
    jeda_waktu_simpan_riwayat = db.Column(db.Integer, default=6)  # dalam jam
