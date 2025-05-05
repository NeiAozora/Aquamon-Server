from flask import request, jsonify
from models.kolam import Kolam
from sqlalchemy.orm import joinedload
from core.db import db
from helpers.auth import decode_token_and_get_user

from core.global_state import iot_command_manager
from helpers.iot_events import *


class KolamController:

    def update_mode_kuras_otomatis(self):
        # Decode token dan validasi pengguna
        auth_result, code = decode_token_and_get_user(request.headers.get("Authorization"))
        if code != 200:
            return jsonify(auth_result), code

        # Ambil data JSON dan validasi formatnya
        data = request.get_json(silent=True)
        if not data or 'id_kolam' not in data or 'mode_otomatis' not in data:
            return jsonify({"message": "Invalid JSON format"}), 400

        id_kolam = data['id_kolam']
        mode_otomatis = data['mode_otomatis']

        # Validasi id_kolam dan mode_otomatis
        if not isinstance(id_kolam, int) or not isinstance(mode_otomatis, bool):
            return jsonify({"message": "Invalid id_kolam or mode_otomatis"}), 400

        # Cari kolam berdasarkan id_kolam
        kolam = db.session.query(Kolam).filter_by(id_kolam=id_kolam).first()
        
        # Jika kolam tidak ditemukan
        if kolam is None:
            return jsonify({"message": "Kolam tidak ditemukan"}), 404
        
        # Update status pengurasan otomatis
        kolam.pengurasan_otomatis = mode_otomatis
        
        # Commit perubahan ke database
        db.session.commit()

        # Kirim respon sukses
        return jsonify({
            "message": "Perintah mode kuras otomatis berhasil diperbarui",
            "id_kolam": id_kolam,
            "mode_otomatis": mode_otomatis
        }), 200
    
    def get_kolam(self, id):
        auth_result, code = decode_token_and_get_user(request)
        if code != 200:
            return jsonify(auth_result), code

        # Validasi ID (harus numeric)
        if not str(id).isnumeric():
            return jsonify({"message": "Invalid kolam id"}), 400

        # Ambil kolam berdasarkan ID
        kolam = db.session.query(Kolam).filter_by(id_kolam=int(id)).options(
            joinedload(Kolam.device_status)
            ).first()

        if not kolam:
            return jsonify({"message": "Kolam not found"}), 404

        # Kembalikan data kolam (bisa disesuaikan dengan field yang ingin ditampilkan)
        return jsonify({
                "id_kolam": kolam.id_kolam,
                "nama_kolam": kolam.nama_kolam,
                "lokasi": kolam.lokasi,
                "deskripsi": kolam.deskripsi,
                "pengurasan_otomatis": kolam.pengurasan_otomatis,
                "status": {
                    "status_online": kolam.device_status.status_online
                } if kolam.device_status else None,
            }), 200
        
        
    def update_keran_mode(self):
        auth_result, code = decode_token_and_get_user(request.headers.get("Authorization"))
        if code != 200:
            return jsonify(auth_result), code

        data = request.get_json(silent=True)
        if not data or 'id_kolam' not in data or 'mode_keran' not in data:
            return jsonify({"message": "Invalid JSON format"}), 400

        id_kolam = data['id_kolam']
        mode_keran = data['mode_keran']  # <== ini akan dikirim sebagai `data`, bukan `tipe`

        if not isinstance(id_kolam, int) or not isinstance(mode_keran, int):
            return jsonify({"message": "Invalid id_kolam or mode_keran"}), 400

        iot_command_manager.set_command(
            id_kolam=id_kolam,
            tipe_jenis_perintah=OPEN_KERAN,  # selalu OPEN_KERAN, karena ini jenis perintah
            data={"mode_keran": mode_keran},  # ini nilai yang ingin di-set (misal: 1=buka, 0=tutup)
            status=PENDING
        )

        return jsonify({
            "message": "Perintah keran dikirim",
            "id_kolam": id_kolam,
            "tipe": OPEN_KERAN,
            "data": {"mode_keran": mode_keran}
        }), 200
        
        
        
    def get_all_kolam(self):
        
        auth_result, code = decode_token_and_get_user(request.headers.get("Authorization"))
        
        if code is not 200:
            return auth_result, code
        
        
        kolam_list = db.session.query(Kolam).options(
            joinedload(Kolam.device_status),
            # joinedload(Kolam.notifikasi),
            # joinedload(Kolam.riwayat_amonia),
            # joinedload(Kolam.riwayat_pengurasan)
        ).all()

        result = []
        for kolam in kolam_list:
            result.append({
                "id_kolam": kolam.id_kolam,
                "nama_kolam": kolam.nama_kolam,
                "lokasi": kolam.lokasi,
                "deskripsi": kolam.deskripsi,
                "pengurasan_otomatis": kolam.pengurasan_otomatis,
                "status": {
                    "status_online": kolam.device_status.status_online
                } if kolam.device_status else None,

            })

        return jsonify(result), 200
