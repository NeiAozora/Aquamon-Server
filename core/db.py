import logging
from flask_sqlalchemy import SQLAlchemy

try:
    # Ini dia: langsung SQLAlchemy instance
    db = SQLAlchemy()
except Exception as e:
    logging.error(f"[DB INIT ERROR] Gagal inisialisasi SQLAlchemy: {e}")
    # Kalau mau, bisa ganti RuntimeError ke custom exception
    raise RuntimeError(f"Database initialization failed: {e}")
