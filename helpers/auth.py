import jwt  # Library untuk encode/decode JWT
from flask import jsonify  # (Tidak digunakan di sini, bisa dihapus)
from models.user import User  # Import model User dari models
from config import SECRET_KEY  # Ambil secret key dari konfigurasi
from datetime import datetime, timedelta


def decode_token_and_get_user(auth_header):
    # Cek apakah Authorization header ada dan dimulai dengan "Bearer "
    if not auth_header or not auth_header.startswith('Bearer '):
        return {'message': 'Token required'}, 401  # Token kosong / salah format

    # Ambil token-nya saja dari header
    token = auth_header.split(' ')[1]

    try:
        # Decode token menggunakan secret key dan algoritma HS256
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])

        # Query user berdasarkan id_user dari payload JWT
        user = User.query.filter_by(id_user=payload['id_user']).first()

        # Jika user ditemukan, kembalikan info user
        if user:
            return {
                'message': 'Token valid',
                'id_user': user.id_user,
                'username': user.username
            }, 200
        else:
            return {'message': 'User not found'}, 404  # ID user tidak cocok
    except jwt.ExpiredSignatureError:
        return {'message': 'Token expired'}, 401  # Token sudah kedaluwarsa
    except jwt.InvalidTokenError:
        return {'message': 'Invalid token'}, 401  # Token tidak valid (salah sign, corrupt, dll)



def generate_token(user):
    payload = {
        'id_user': user.id_user,
        'username': user.username,
        'exp': datetime.utcnow() + timedelta(hours=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token