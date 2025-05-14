from datetime import datetime
from threading import Lock
from helpers.iot_events import *

class AmoniaStatusCache:
    def __init__(self):
        self._cache = {}  # {id_kolam: {'nilai': float, 'terakhir': datetime}}
        self._lock = Lock()

    def update(self, id_kolam, nilai, cooldown_ms_tersisa, keran_dibuka):
        with self._lock:
            self._cache[id_kolam] = {
                'nilai': nilai,
                'terakhir': datetime.now(),
                'cooldown_tersisa' : cooldown_ms_tersisa,
                'keran_dibuka' : keran_dibuka
            }

    def get(self, id_kolam):
        return self._cache.get(id_kolam)

    def clear_cache(self, id_kolam):
        with self._lock:
            if id_kolam in self._cache:
                del self._cache[id_kolam]

    def get_all(self):
        return dict(self._cache)



class IOTCommandManager:
    def __init__(self):
        self._commands = {}  # {id_kolam: {'tipe': int, 'data': {}, 'status': str}}
        self._lock = Lock()

    def set_command(self, id_kolam, tipe_jenis_perintah, data, status=PENDING):
        with self._lock:
            self._commands[id_kolam] = {
                'tipe': tipe_jenis_perintah,
                'data': data,
                'status': status
            }

    def get_command(self, id_kolam):
        return self._commands.get(id_kolam)

    def update_status(self, id_kolam, status):
        with self._lock:
            if id_kolam in self._commands:
                self._commands[id_kolam]['status'] = status

    def clear_command(self, id_kolam):
        with self._lock:
            if id_kolam in self._commands:
                del self._commands[id_kolam]

    def get_all(self):
        return dict(self._commands)


# Singleton instances (bisa langsung di-import dan dipakai)
amonia_cache = AmoniaStatusCache()
iot_command_manager = IOTCommandManager()


