import asyncio  # Untuk asynchronous loop
from datetime import datetime, timedelta  # Untuk manipulasi waktu
from sqlalchemy.orm import joinedload  # Untuk eager loading relasi SQLAlchemy

# Impor modul internal dari proyek
from core.db import db  # SQLAlchemy session
from core.logger import logger  # Logger untuk mencatat aktivitas
from core.global_state import amonia_cache, iot_command_manager  # Cache kadar amonia & manajemen perintah IoT
from helpers.iot_events import OPEN_KERAN  # Konstanta perintah membuka keran

# Model-model SQLAlchemy
from models.kolam import Kolam
from models.user_settings import UserSettings
from models.riwayat_amonia import RiwayatAmonia
from models.notifikasi import Notifikasi


class AmoniaChecker:
    def __init__(self, app):
        self._app = app  # Simpan objek Flask app untuk akses context
        self._logger = logger  # Logger untuk mencetak log

    async def run(self):
        # Jalankan dalam konteks Flask agar bisa akses ke database dan session
        with self._app.app_context():
            while True:  # Loop terus-menerus (background service)
                self._logger.info("🔄 Service check amonia Berjalan...")  # Log info

                settings = self._get_settings()  # Ambil pengaturan pengguna
                if settings:  # Hanya lanjut kalau settings ditemukan
                    self._proses_riwayat(settings.jeda_waktu_simpan_riwayat)  # Simpan riwayat amonia jika waktunya
                    self._proses_amonia(settings.batasan_amonia)  # Cek apakah kadar amonia melewati batas

                await asyncio.sleep(5)  # Delay 5 detik sebelum loop berikutnya

    def _get_settings(self):
        # Ambil satu baris pengaturan dari database
        settings = db.session.query(UserSettings).first()
        if not settings:
            self._logger.warning("⚠️ User settings not found, skipping...")  # Log jika tidak ada
        return settings

    def _proses_riwayat(self, jeda_menit):
        now = datetime.utcnow()  # Ambil waktu saat ini dalam UTC
        # Ambil semua kolam dan riwayatnya (eager loading)
        kolam_list = db.session.query(Kolam).options(joinedload(Kolam.riwayat_amonia)).all()

        riwayat_baru = []  # Buffer untuk riwayat yang akan disimpan sekaligus

        for kolam in kolam_list:
            # Ambil entri terakhir dari riwayat kolam ini
            last_entry = (
                db.session.query(RiwayatAmonia)
                .filter_by(id_kolam=kolam.id_kolam)
                .order_by(RiwayatAmonia.waktu_pencatatan.desc())
                .first()
            )

            # Cek apakah waktunya untuk mencatat riwayat baru
            if not last_entry or (now - last_entry.waktu_pencatatan) >= timedelta(minutes=jeda_menit):
                nilai_amonia = amonia_cache.get(kolam.id_kolam)  # Ambil kadar amonia dari cache
                if nilai_amonia is not None:
                    # Tambahkan ke buffer
                    riwayat_baru.append(
                        RiwayatAmonia(
                            id_kolam=kolam.id_kolam,
                            kadar_amonia=nilai_amonia,
                            waktu_pencatatan=now
                        )
                    )
                    self._logger.info(f"📥 Riwayat amonia dicatat untuk Kolam {kolam.id_kolam}: {nilai_amonia}")

        # Simpan semua entri baru sekaligus jika ada
        if riwayat_baru:
            db.session.add_all(riwayat_baru)
            db.session.commit()

    # Method untuk melakukan proses amonia dari IOT yang tersambung
    def _proses_amonia(self, batas_amonia):
        caches = amonia_cache.get_all()  # Ambil seluruh cache amonia dari state
        now = datetime.utcnow()  # Waktu sekarang
        notifikasi_list = []  # Buffer notifikasi yang akan dikirim

        for id_kolam, cache in caches.items():
            if cache["nilai"] < batas_amonia:  # Lewati jika masih di bawah batas
                continue

            # Log peringatan kadar tinggi
            self._logger.warning(f"⚠️ Amonia level exceeded for Kolam {id_kolam}: {cache['nilai']}")

            kolam = db.session.query(Kolam).filter_by(id_kolam=id_kolam).first()  # Ambil data kolam
            if not kolam:
                continue  # Lewati jika kolam tidak ditemukan

            # Tambahkan notifikasi peringatan ke buffer
            notifikasi_list.append(
                Notifikasi(
                    id_kolam=id_kolam,
                    judul="Peringatan",
                    pesan=f"Kadar Amonia Melebihi Batas Normal. Segera lakukan pengurasan Kolam {id_kolam}.",
                    dibaca=False,
                    waktu_dibuat=now
                )
            )

            if kolam.pengurasan_otomatis:
                # Kirim perintah IoT untuk membuka keran
                iot_command_manager.set_command(
                    id_kolam=id_kolam,
                    tipe_jenis_perintah=OPEN_KERAN,
                    data={},
                    status="PENDING"
                )
                self._logger.info(f"🔧 Command to open drain sent for Kolam {id_kolam}")

                # Tambahkan notifikasi bahwa sistem menguras otomatis
                notifikasi_list.append(
                    Notifikasi(
                        id_kolam=id_kolam,
                        judul="Pemberitahuan",
                        pesan=f"Pengurasan otomatis telah dilakukan di Kolam {id_kolam} karena kadar amonia tinggi.",
                        dibaca=False,
                        waktu_dibuat=now
                    )
                )

        # Commit semua notifikasi sekaligus
        if notifikasi_list:
            db.session.add_all(notifikasi_list)
            db.session.commit()
