from flask import request, jsonify
from datetime import datetime, timedelta
from models.riwayat_amonia import RiwayatAmonia
from models.user_settings import UserSettings
from core.db import db
from core.global_state import amonia_cache, iot_command_manager
from helpers.auth import decode_token_and_get_user

class KolamController:
    def get_kolam_setting(self):

        # Semua IOT menggunakan satu setting yang sama
        setting = db.session.query(UserSettings).first()
        if not setting:
            return jsonify({"message": "User settings not configured"}), 500

        return jsonify({"batas_amonia": setting.batasan_amonia}), 200

    def update_status(self):

        data = request.get_json(silent=True)
        if not data or 'id_kolam' not in data or 'nilai_amonia' not in data:
            return jsonify({"error": "id_kolam dan nilai_amonia wajib diisi"}), 400

        id_kolam = data['id_kolam']
        nilai_amonia = data['nilai_amonia']

        # Validasi tipe input
        if not isinstance(id_kolam, int) or not isinstance(nilai_amonia, (int, float)):
            return jsonify({"error": "Invalid id_kolam or nilai_amonia type"}), 400

        # Update cache tanpa simpan DB
        amonia_cache.update_status(id_kolam, nilai_amonia)

        return jsonify({"message": "Status amonia diperbarui"}), 200

    def get_command(self):

        data = request.get_json(silent=True)
        if not data or 'id_kolam' not in data:
            return jsonify({"error": "id_kolam wajib diisi"}), 400

        id_kolam = data['id_kolam']

        # Ambil perintah yang aktif untuk kolam tersebut
        command = iot_command_manager.get_command(id_kolam)
        
        if not command:
            return jsonify({"message": f"Tidak ada perintah aktif untuk kolam {id_kolam}"}), 404

        return jsonify({
            "id_kolam": id_kolam,
            "command": command
        }), 200

    def _simpan_ke_db(self, id_kolam: int, nilai_amonia: float, waktu: datetime):
        """
        Menyimpan data amonia ke dalam tabel riwayat_amonia.
        """
        riwayat = RiwayatAmonia(
            id_kolam=id_kolam,
            kadar_amonia=nilai_amonia,
            waktu_pencatatan=waktu
        )
        db.session.add(riwayat)
        db.session.commit()
