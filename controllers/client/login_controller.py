import jwt
import bcrypt
from flask import Flask, request, jsonify
from core.db import db  # your db
from models.user import User  # make sure to import User properly
from helpers.auth import decode_token_and_get_user, generate_token

from config import SECRET_KEY


class LoginController:

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
            token = generate_token(user)
            return jsonify({
                'message': 'Login successful',
                'token': token
            }), 200
        else:
            return jsonify({'message': 'Invalid username or password'}), 401

    def token_auth(self):
        auth_header = request.headers.get('Authorization')
        user_data, status_code = decode_token_and_get_user(auth_header)

        return jsonify(user_data), status_code