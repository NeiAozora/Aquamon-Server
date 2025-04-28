from core.db import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'

    id_user = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(65), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    nomer_telpon = db.Column(db.String(15))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
