import bcrypt

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
    
    server = Server
    
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

    
        password = "fauzan"
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        user = User(
            name="Ahmad Fauzan", 
            username="Fauzan", 
            password=hashed_password, 
            nomer_telepon="083119624458"
        )
        
        user_settings = UserSettings(
            batasan_amonia = 390,
            jeda_waktu_simpan_riwayat = 60 * 3
        )
        
        kolam_1 = Kolam(
            id_kolam = 1,
            id_user = 1,
            nama_kolam = "Kolam Lele 1",
            lokasi = "",
            deskripsi = "Tidak ada deskripsi",
            pengurasan_otomatis = True
        )
        
        kolam_2 = Kolam(
            id_kolam = 2,
            id_user = 1,
            nama_kolam = "Kolam Lele 1",
            lokasi = "",
            deskripsi = "Tidak ada deskripsi",
            pengurasan_otomatis = True
        )
        
        notifikasi = Notifikasi(
            id_notifikasi = 1,
            id_kolam = 1,
            judul = 
            pesan =
            dibaca = False
            waktu_dibuat = 
        ) 
        
        device_status_kolam_1 = DeviceStatus(
            id_status = 1,
            id_kolam = 1,
            status_online = False
        )
        
        device_status_kolam_2 = DeviceStatus(
            id_status = 2,
            id_kolam = 2,
            status_online = False,
        )
        
        

        seeds = []

        db.session.add_all(seed)
        db.session.commit()

        print("Database seeded!")

if __name__ == '__main__':
    seed()
