from core.db import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'

    id_user = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(65), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    nomer_telepon = db.Column(db.String(15))
    foto_profil = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    kolam_list = db.relationship('Kolam', backref='user', cascade="all, delete-orphan")
    settings = db.relationship('UserSettings', backref='user', cascade="all, delete-orphan", uselist=False)
