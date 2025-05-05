from flask import render_template
from flask import Blueprint
from flask import Response
from core.route import Route
from core.logger import Logger
from controllers.client.login_controller import LoginController;
from controllers.iot.kolam_controller import KolamController as IOTKolamController
from controllers.client.register_controller import RegisterController
from controllers.client.kolam_controller import KolamController as ClientKolamController
from controllers.client.notifikasi_controller import NotifikasiController
from controllers.client.riwayat_pengecekan_controller import RiwayatPengecekanController
from controllers.client.pengaturan_controller import PengaturanController


def test():
    Logger.get_logger().debug("Ping!")
    
    res = Response()
    res.status = 200
    return res



def register_routes(app):
    route = Route(app)

    # Test endpoint
    route.get("/api/ping", test)

    # CLIENT SIDE ROUTES

    # AUTH
    route.post("/api/client/auth/login", LoginController, "login")
    route.post("/api/client/auth/register", RegisterController, "register")
    route.post("/api/client/auth/token", LoginController, "token_auth")

    # KOLAM
    route.get("/api/client/kolam", ClientKolamController, "get_all_kolam")  # get all ponds
    route.get("/api/client/kolam/<id>", ClientKolamController, "get_kolam")  # get single pond
    route.put("/api/client/kolam/<id>/auto-flush", ClientKolamController, "update_mode_kuras_otomatis")  # update auto flush
    route.put("/api/client/kolam/<id>/valve-mode", ClientKolamController, "update_keran_mode")  # update valve mode

    # NOTIFIKASI
    route.get("/api/client/notifications", NotifikasiController, "get_all")
    route.delete("/api/client/notifications/<id>", NotifikasiController, "delete")
    route.put("/api/client/notifications/<id>/read-status", NotifikasiController, "update_status_dibaca")

    # RIWAYAT PENGECEKAN AMONIA
    route.get("/api/client/amonia-history", RiwayatPengecekanController, "get_riwayat")
    route.get("/api/client/amonia-history/<id>", RiwayatPengecekanController, "get_riwayat")
    route.delete("/api/client/amonia-history/<id>", RiwayatPengecekanController, "delete")

    # PENGATURAN
    route.get("/api/client/settings", PengaturanController, "get_settings")
    route.put("/api/client/settings", PengaturanController, "update_settings")

    # IOT SIDE ROUTES

    route.put("/api/iot/status", IOTKolamController, "update_status")
    route.get("/api/iot/settings", IOTKolamController, "get_kolam_settings")
    route.get("/api/iot/commands", IOTKolamController, "get_commands")
