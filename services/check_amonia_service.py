import asyncio
from core.global_state import amonia_cache, iot_command_manager
from models.user_settings import UserSettings
from models.kolam import Kolam
from models.notifikasi import Notifikasi
from models.riwayat_amonia import RiwayatAmonia
from sqlalchemy.orm import joinedload
from sqlalchemy import asc
from core.db import db
from core.server import get_global_server, set_global_server
from helpers.iot_events import OPEN_KERAN, CLOSE_KERAN
from datetime import datetime, timedelta
from flask import Flask
from config import *

import queue
from config import HOST_DEVELOPMENT
from core.server import Server

comm_queue = queue.Queue()

comm_queue.put("get_value")  # Request to get shared value
logger = comm_queue.get()  # Retrieve shared value

init_done = False

def init_server():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

async def check_amonia_worker():
    global init_done

    if not init_done:
        init_server()
        init_done = True
    
    while True:

        
        logger.info("🔄 Service check amonia Berjalan...")

        # Disini akan melakukan check cache amonia, jika melebihi batas, maka akan melakukan notifikasi ke peternak, 
        # dan melakukan tugas berdasarkan pengaturan apakah akan melakukan pengurasan otomatis atau tidak
        # Sekaligus akan melakukan simpan riwayat berdasar jeda di settings
        
        settings = db.session.query(UserSettings).first()
        if not settings:
            logger.warning("⚠️ User settings not found, skipping...")
            await asyncio.sleep(5)
            continue
        
        waktu_jeda_menit = settings.jeda_waktu_simpan_riwayat

        # Pelaporan riwayat ke DB.Riwayat Amonia secara berkala
        semua_kolam = db.session.query(Kolam).options(
            joinedload(Kolam.riwayat_amonia)
        ).all()

        now = datetime.utcnow()
        
        for kolam in semua_kolam:
            last_entry = (
                db.session.query(RiwayatAmonia)
                .filter_by(id_kolam=kolam.id_kolam)
                .order_by(RiwayatAmonia.waktu_pencatatan.desc())
                .first()
            )

            should_insert = False

            if not last_entry:
                should_insert = True
            else:
                delta = now - last_entry.waktu_pencatatan
                if delta >= timedelta(minutes=waktu_jeda_menit):
                    should_insert = True

            if should_insert:
                nilai_amonia = amonia_cache.get(kolam.id_kolam)
                if nilai_amonia is not None:
                    riwayat = RiwayatAmonia(
                        id_kolam=kolam.id_kolam,
                        kadar_amonia=nilai_amonia,
                        waktu_pencatatan=now
                    )
                    db.session.add(riwayat)
                    db.session.commit()
                    logger.info(f"📥 Riwayat amonia dicatat untuk Kolam {kolam.id_kolam}: {nilai_amonia}")
        
        # Get all cached ammonia status data
        caches = amonia_cache.get_all()
        
        for id_kolam, cache in caches.items():
            # Check if ammonia level exceeds the threshold
            if cache["nilai"] >= settings.batasan_amonia:
                logger.warning(f"⚠️ Amonia level exceeded for Kolam {id_kolam}: {cache['nilai']}")

                kolam = db.session.query(Kolam).filter_by(id_kolam=id_kolam).first()
                if kolam:
                    notifikasi = Notifikasi(
                        id_notifikasi=None,
                        id_kolam=id_kolam,
                        judul="Peringatan",
                        pesan=f"Kadar Amonia Melebihi Batas Normal Segera Lakukan Pengursan Kolam {id_kolam} Butuh Untuk Segera Dikuras",
                        dibaca=False,
                        waktu_dibuat=datetime.utcnow()
                    )
                    db.session.add(notifikasi)
                    db.session.commit()

                    if kolam.pengurasan_otomatis:
                        iot_command_manager.set_command(
                            id_kolam=id_kolam,
                            tipe_jenis_perintah=OPEN_KERAN,
                            data={},
                            status="PENDING"
                        )
                        logger.info(f"🔧 Command to open drain sent for Kolam {id_kolam}")

                        notifikasi_auto = Notifikasi(
                            id_notifikasi=None,
                            id_kolam=id_kolam,
                            judul="Pemberitahuan",
                            pesan=f"Kadar Amonia Melebihi Batas Normal Di Kolam {id_kolam}, Pengurasan otomatis telah dilakukan",
                            dibaca=False,
                            waktu_dibuat=datetime.utcnow()
                        )
                        db.session.add(notifikasi_auto)
                        db.session.commit()
        
        # Wait for 5 seconds before checking again
        await asyncio.sleep(5)
