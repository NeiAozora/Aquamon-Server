from flask import jsonify, request
from models.user import User
from core.db import db

class UserController:
    @staticmethod
    def get_all_users():
        users = User.query.all()
        return jsonify([user.serialize() for user in users])

    @staticmethod
    def get_user(user_id):
        user = User.query.get(user_id)
        if user:
            return jsonify(user.serialize())
        return jsonify({"message": "User not found"}), 404

    @staticmethod
    def create_user():
        data = request.get_json()
        new_user = User(
            name=data['name'],
            username=data['username'],
            password_hash=data['password_hash'],
            nomer_telpon=data.get('nomer_telpon'),
            created_at=data.get('created_at')
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.serialize()), 201

    @staticmethod
    def update_user(user_id):
        user = User.query.get(user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404
        
        data = request.get_json()
        user.name = data.get('name', user.name)
        user.username = data.get('username', user.username)
        user.password_hash = data.get('password_hash', user.password_hash)
        user.nomer_telpon = data.get('nomer_telpon', user.nomer_telpon)
        db.session.commit()
        return jsonify(user.serialize())

    @staticmethod
    def delete_user(user_id):
        user = User.query.get(user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"})
