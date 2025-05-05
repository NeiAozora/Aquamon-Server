from flask import request, jsonify
from core.db import db
from models.user_settings import UserSettings
from models.user import User
from helpers.auth import decode_token_and_get_user

class PengaturanController:

    def get_settings(self):
        auth_result, code = decode_token_and_get_user(request.headers.get("Authorization"))
        if code != 200:
            return jsonify(auth_result), code

        user = db.session.query(User).filter_by(id_user=auth_result['id_user']).first()
        if not user or not user.settings:
            return jsonify({"message": "User settings not found"}), 404

        s = user.settings
        return jsonify({
            "id_setting": s.id_setting,
            "id_user":    s.id_user,
            "batasan_amonia":         s.batasan_amonia,
            "jeda_waktu_simpan_riwayat": s.jeda_waktu_simpan_riwayat
        }), 200

    def update_settings(self):
        auth_result, code = decode_token_and_get_user(request.headers.get("Authorization"))
        if code != 200:
            return jsonify(auth_result), code

        data = request.get_json(silent=True)
        if not data:
            return jsonify({"message": "Invalid JSON format"}), 400

        user = db.session.query(User).filter_by(id_user=auth_result['id_user']).first()
        if not user or not user.settings:
            return jsonify({"message": "User settings not found"}), 404

        s = user.settings
        if 'batasan_amonia' in data:
            s.batasan_amonia = data['batasan_amonia']
        if 'jeda_waktu_simpan_riwayat' in data:
            s.jeda_waktu_simpan_riwayat = data['jeda_waktu_simpan_riwayat']

        db.session.commit()
        return jsonify({"message": "Settings updated"}), 200
