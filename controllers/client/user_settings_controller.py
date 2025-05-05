from flask import request, jsonify
from core.db import db
from models.user import User
from helpers.auth import decode_token_and_get_user

class UserController:
    def get_user_details(self):
        # Decode token and get the user
        auth_result, code = decode_token_and_get_user(request.headers.get("Authorization"))
        if code != 200:
            return jsonify(auth_result), code

        # Fetch the user from the database
        user = db.session.query(User).filter_by(id_user=auth_result['id_user']).first()
        if not user:
            return jsonify({"message": "User not found"}), 404

        # Return user details
        return jsonify({
            "id_user": user.id_user,
            "name": user.name,
            "username": user.username,
            "nomer_telepon": user.nomer_telepon,
            "foto_profil": user.foto_profil,
            "created_at": user.created_at
        }), 200

    def update_user_details(self):
        # Decode token and get the user
        auth_result, code = decode_token_and_get_user(request.headers.get("Authorization"))
        if code != 200:
            return jsonify(auth_result), code

        # Get the data from request
        data = request.get_json(silent=True) or {}
        
        # Fields to be updated
        upd = {}
        if 'name' in data:
            upd['name'] = data['name']
        if 'username' in data:
            upd['username'] = data['username']
        if 'nomer_telepon' in data:
            upd['nomer_telepon'] = data['nomer_telepon']
        if 'foto_profil' in data:
            upd['foto_profil'] = data['foto_profil']

        # Ensure there are valid fields to update
        if not upd:
            return jsonify({"message": "No valid fields to update"}), 400

        # Fetch the user from the database
        user = db.session.query(User).filter_by(id_user=auth_result['id_user']).first()
        if not user:
            return jsonify({"message": "User not found"}), 404

        # Update user fields
        for k, v in upd.items():
            setattr(user, k, v)

        # Commit the changes to the database
        db.session.commit()

        return jsonify({"message": "User details updated successfully"}), 200
