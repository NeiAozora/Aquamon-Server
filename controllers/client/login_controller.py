import jwt
import bcrypt
from flask import Flask, request, jsonify
from core.db import db  # your db
from datetime import datetime, timedelta
from models.user import User  # make sure to import User properly

from config import SECRET_KEY


class LoginController:
    def generate_token(self, user):
        payload = {
            'id_user': user.id_user,
            'username': user.username,
            'exp': datetime.utcnow() + timedelta(hours=1)  # expires in 1 hour
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return token

    def check_password(self, hashed_password, password):
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

    def login(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'message': 'Username and password required'}), 400

        user = User.query.filter_by(username=username).first()

        if user and self.check_password(user.password, password):
            token = self.generate_token(user)
            return jsonify({
                'message': 'Login successful',
                'token': token
            }), 200
        else:
            return jsonify({'message': 'Invalid username or password'}), 401