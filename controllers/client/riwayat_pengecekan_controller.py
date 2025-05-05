from flask import request, jsonify
from datetime import datetime
from core.db import db
from models.riwayat_amonia import RiwayatAmonia
from models.kolam import Kolam
from helpers.auth import decode_token_and_get_user
from sqlalchemy.exc import SQLAlchemyError


class RiwayatPengecekanController:
    
    # Create - Menambahkan riwayat amonia baru
    def create_riwayat(self):
        auth_result, code = decode_token_and_get_user(request.headers.get("Authorization"))
        if code != 200:
            return jsonify(auth_result), code
        
        # Ambil data JSON
        data = request.get_json(silent=True)
        if not data or 'id_kolam' not in data or 'kadar_amonia' not in data:
            return jsonify({"message": "Invalid JSON format"}), 400
        
        id_kolam = data['id_kolam']
        kadar_amonia = data['kadar_amonia']

        if not isinstance(id_kolam, int) or not isinstance(kadar_amonia, (float, int)):
            return jsonify({"message": "Invalid data types"}), 400

        # Validasi apakah kolam ada
        kolam = db.session.query(Kolam).filter_by(id_kolam=id_kolam).first()
        if not kolam:
            return jsonify({"message": "Kolam tidak ditemukan"}), 404
        
        # Membuat riwayat amonia baru
        try:
            riwayat_amonia = RiwayatAmonia(
                id_kolam=id_kolam,
                kadar_amonia=kadar_amonia,
                waktu_pencatatan=datetime.utcnow()
            )
            db.session.add(riwayat_amonia)
            db.session.commit()
            return jsonify({
                "message": "Riwayat amonia berhasil dibuat",
                "id_riwayat": riwayat_amonia.id_riwayat
            }), 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({"message": str(e)}), 500

    # Read - Mengambil riwayat amonia berdasarkan id_kolam
    def get_riwayat(self, id_kolam = None):
        auth_result, code = decode_token_and_get_user(request.headers.get("Authorization"))
        if code != 200:
            return jsonify(auth_result), code

        if not isinstance(id_kolam, int):
            return jsonify({"message": "Invalid id_kolam"}), 400

        # Query riwayat amonia berdasarkan id_kolam
        riwayat_amonia = db.session.query(RiwayatAmonia).filter_by(id_kolam=id_kolam).all()
        if not riwayat_amonia:
            return jsonify({"message": "Riwayat amonia tidak ditemukan"}), 404

        # Mengembalikan data riwayat amonia
        return jsonify([{
            "id_riwayat": riwayat.id_riwayat,
            "id_kolam": riwayat.id_kolam,
            "kadar_amonia": riwayat.kadar_amonia,
            "waktu_pencatatan": riwayat.waktu_pencatatan.isoformat()
        } for riwayat in riwayat_amonia]), 200

    # Delete - Menghapus riwayat amonia berdasarkan id_riwayat
    def delete_riwayat(self, id_riwayat):
        auth_result, code = decode_token_and_get_user(request.headers.get("Authorization"))
        if code != 200:
            return jsonify(auth_result), code
        
        # Cari riwayat amonia berdasarkan id_riwayat
        riwayat_amonia = db.session.query(RiwayatAmonia).filter_by(id_riwayat=id_riwayat).first()
        if not riwayat_amonia:
            return jsonify({"message": "Riwayat amonia tidak ditemukan"}), 404
        
        # Hapus riwayat amonia
        try:
            db.session.delete(riwayat_amonia)
            db.session.commit()
            return jsonify({"message": "Riwayat amonia berhasil dihapus"}), 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({"message": str(e)}), 500
