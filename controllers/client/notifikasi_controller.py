from flask import request, jsonify
from datetime import datetime
from core.db import db
from models.notifikasi import Notifikasi
from helpers.auth import decode_token_and_get_user
from sqlalchemy.exc import SQLAlchemyError




class NotifikasiController:
    
    def delete(self):
        # Autentikasi user
        auth_result, code = decode_token_and_get_user(request)
        if code != 200:
            return jsonify(auth_result), code

        data = request.get_json(silent=True)
        if not data or 'id_notifikasi' not in data:
            return jsonify({"error": "id_notifikasi wajib diisi"}), 400

        id_notifikasi = data['id_notifikasi']

        # Cari notifikasi berdasarkan id
        notifikasi = Notifikasi.query.get(id_notifikasi)
        if not notifikasi:
            return jsonify({"error": "Notifikasi tidak ditemukan"}), 404

        # Hapus notifikasi
        db.session.delete(notifikasi)
        db.session.commit()

        return jsonify({"message": "Notifikasi berhasil dihapus"}), 200

    def get_all(self):
        # Autentikasi user
        auth_result, code = decode_token_and_get_user(request)
        if code != 200:
            return jsonify(auth_result), code

        # Ambil semua notifikasi
        notifikasis = Notifikasi.query.all()

        # Format response
        response = [{
            "id_notifikasi": n.id_notifikasi,
            "id_kolam": n.id_kolam,
            "judul": n.judul,
            "pesan": n.pesan,
            "dibaca": n.dibaca,
            "waktu_dibuat": n.waktu_dibuat.strftime('%Y-%m-%d %H:%M:%S')
        } for n in notifikasis]

        return jsonify(response), 200

    def update_status_dibaca(self):
        # Autentikasi user
        auth_result, code = decode_token_and_get_user(request)
        if code != 200:
            return jsonify(auth_result), code

        data = request.get_json(silent=True)
        if not data or 'id_notifikasi' not in data:
            return jsonify({"error": "id_notifikasi wajib diisi"}), 400

        id_notifikasi = data['id_notifikasi']

        # Cari notifikasi berdasarkan id
        notifikasi = Notifikasi.query.get(id_notifikasi)
        if not notifikasi:
            return jsonify({"error": "Notifikasi tidak ditemukan"}), 404

        # Perbarui status dibaca menjadi True
        notifikasi.dibaca = True
        db.session.commit()

        return jsonify({"message": "Status notifikasi berhasil diperbarui menjadi dibaca"}), 200
