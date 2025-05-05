import bcrypt
from datetime import datetime

from core.server import Server
from core.db import db

from models.user import User
from models.device_status import DeviceStatus
from models.kolam import Kolam
from models.notifikasi import Notifikasi
from models.riwayat_amonia import RiwayatAmonia
from models.riwayat_pengurasan import RiwayatPengurasan
from models.user_settings import UserSettings


def seed():
    server = Server()

    with server.app.app_context():
        db.drop_all()

        models = [
            User,
            UserSettings,
            Kolam,
            Notifikasi,
            DeviceStatus,
            RiwayatAmonia,
            RiwayatPengurasan
        ]

        for model in models:
            model.__table__.create(db.engine, checkfirst=True)

        password = "fauzan123"
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        user = User(
            name="Ahmad Fauzan", 
            username="fauzan", 
            password=hashed_password, 
            nomer_telepon="083119624458"
        )

        user_settings = UserSettings(
            id_user = 1,
            batasan_amonia=390,
            jeda_waktu_simpan_riwayat=60 * 3
        )

        kolam_1 = Kolam(
            id_kolam=1,
            id_user=1,
            nama_kolam="Kolam Lele 1",
            lokasi="",
            deskripsi="Tidak ada deskripsi",
            pengurasan_otomatis=True
        )

        kolam_2 = Kolam(
            id_kolam=2,
            id_user=1,
            nama_kolam="Kolam Lele 2",
            lokasi="",
            deskripsi="Tidak ada deskripsi",
            pengurasan_otomatis=True
        )

        notifikasi_1 = Notifikasi(
            id_notifikasi=1,
            id_kolam=1,
            judul="Peringatan",
            pesan="Kadar Amonia Melebihi Batas Normal Segera Lakukan Pengursan Kolam 1 Butuh Untuk Segera Dikuras",
            dibaca=False,
            waktu_dibuat=datetime.utcnow()
        )

        notifikasi_2 = Notifikasi(
            id_notifikasi=2,
            id_kolam=2,
            judul="Pemberitahuan",
            pesan="Kadar Amonia Melebihi Batas Normal Di Kolam 2, Pengurasan otomatis telah dilakukan",
            dibaca=False,
            waktu_dibuat=datetime.utcnow()
        )

        device_status_kolam_1 = DeviceStatus(
            id_status=1,
            id_kolam=1,
            status_online=False
        )

        device_status_kolam_2 = DeviceStatus(
            id_status=2,
            id_kolam=2,
            status_online=False
        )

        seeds = (
            user,
            user_settings,
            kolam_1,
            kolam_2,
            notifikasi_1,
            notifikasi_2,
            device_status_kolam_1,
            device_status_kolam_2
        )

        db.session.add_all(seeds)
        db.session.commit()

        print("Database seeded!")


if __name__ == '__main__':
    seed()
