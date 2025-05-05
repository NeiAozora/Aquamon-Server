import jwt
import bcrypt
from flask import request, jsonify, Response
from datetime import datetime, timedelta
from core.db import db
from models.user import User
from config import SECRET_KEY


class RegisterController:
    def generate_token(self, user):
        payload = {
            'id_user': user.id_user,
            'username': user.username,
            'exp': datetime.utcnow() + timedelta(hours=1)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return token

    def hash_password(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def register(self):
        data = request.get_json()
        name = data.get('name')
        username = data.get('username')
        password = data.get('password')
        nomer_telepon = data.get('nomer_telepon')

        if not all([name, username, password]):
            return jsonify({'message': 'Name, username, and password are required'}), 400

        if User.query.filter_by(username=username).first():
            return jsonify({'message': 'Username already taken'}), 409

        hashed_password = self.hash_password(password)
        new_user = User(
            name=name,
            username=username,
            password=hashed_password,
            nomer_telepon=nomer_telepon
        )
        db.session.add(new_user)
        db.session.commit()

        token = self.generate_token(new_user)
        return jsonify({
            'message': 'Registration successful',
            'token': token
        }), 201
