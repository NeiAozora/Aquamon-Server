from models.riwayat_amonia import RiwayatAmonia
from core.db import db
from core.logger import logger
from datetime import datetime
from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError

def create_riwayat(id_kolam, kadar_amonia):
            # Membuat riwayat amonia baru
    try:
        riwayat_amonia = RiwayatAmonia(
            id_kolam=id_kolam,
            kadar_amonia=kadar_amonia,
            waktu_pencatatan=datetime.utcnow()
        )
        db.session.add(riwayat_amonia)
        db.session.commit()
        logger.info(f"Riwayat amonia kolam ID: {id_kolam} berhasil dibuat")

    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(str(e))
