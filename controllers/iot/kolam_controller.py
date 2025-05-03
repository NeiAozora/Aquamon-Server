from flask import request
from datetime import datetime, timedelta
from models.riwayat_amonia import RiwayatAmonia
from models.user_settings import  UserSettings
from core.db import db
from core.global_var import status_amonia_terakhir

class KolamController:
    
    def get_kolam_setting(self):
        # pukul rata semua iot konfigurasi sama, setiap IOT akan melakukan update setiap 10 detik unutk mendapatkan data
        setting = db.session.query(UserSettings).first()
        
        nilai = setting.batasan_amonia
        
        return {"batas_amonia" : nilai},200
    
    def update_status(self):
        # Ambil data JSON dari request POST
        data = request.get_json()
        id_kolam = data.get("id_kolam")
        nilai_amonia = data.get("nilai_amonia")

        # Validasi input wajib
        if id_kolam is None or nilai_amonia is None:
            return {"error": "id_kolam dan nilai_amonia wajib diisi"}, 400

        sekarang = datetime.utcnow()
        global status_amonia_terakhir

        # Ambil status terakhir dari cache global
        status = status_amonia_terakhir.get(id_kolam)

        if status is None:
            # Jika belum pernah tercatat, langsung simpan ke DB
            self._simpan_ke_db(id_kolam, nilai_amonia, sekarang)
            status_amonia_terakhir[id_kolam] = {'nilai': nilai_amonia, 'terakhir': sekarang}
        else:
            terakhir = status['terakhir']
            # Simpan ke DB hanya jika sudah lewat 3 jam sejak pencatatan terakhir
            if sekarang - terakhir >= timedelta(hours=3):
                self._simpan_ke_db(id_kolam, nilai_amonia, sekarang)
                status_amonia_terakhir[id_kolam] = {'nilai': nilai_amonia, 'terakhir': sekarang}
            else:
                # Jika belum waktunya, hanya update nilai di cache
                status_amonia_terakhir[id_kolam]['nilai'] = nilai_amonia

        return {"message": "Status amonia diperbarui"}, 200

    def _simpan_ke_db(self, id_kolam: int, nilai_amonia: float, waktu: datetime):
        """
        Menyimpan data amonia ke dalam tabel riwayat_amonia.
        """
        riwayat = RiwayatAmonia(
            id_kolam=id_kolam,
            kadar_amonia=nilai_amonia,
            waktu_pencatatan=waktu
        )
        db.session.add(riwayat)
        db.session.commit()
