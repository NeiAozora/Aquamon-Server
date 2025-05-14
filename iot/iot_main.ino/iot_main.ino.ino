#include <ESP32Servo.h>
#include <WiFi.h>
#include <ArduinoJson.h>
#include <HTTPClient.h>

// ======== Konstanta untuk Jenis Perintah dari Server ========
#define OPEN_KERAN 1              // Buka servo (keran terbuka)
#define CLOSE_KERAN 2             // Tutup servo (keran tertutup)
#define UPDATE_BATAS_NH3 3        // Update nilai ambang amonia

// ======== Konstanta untuk Status Perintah dari Server ========
#define PENDING 11
#define SUCCESS 12
#define FAILED 13

// ======== Konfigurasi WiFi dan Server ========
const char* SSID = "WIFI_KAMU";             // Ganti dengan SSID WiFi
const char* PASSWORD = "PASSWORD_KAMU";     // Ganti dengan Password WiFi

const char* BASE_URL = "http://example.com";  // URL server backend
const char* endpointStatus = "/api/iot/status";       // Endpoint POST status kadar amonia
const char* endpointSettings = "/api/iot/settings";   // Endpoint GET pengaturan ambang NH3
const char* endpointCommands = "/api/iot/1/commands/"; // Endpoint GET perintah untuk IoT

const int ID_KOLAM = 1;  // ID kolam, dikirim saat upload data

// ======== Kelas SensorAmonia ========
// Bertanggung jawab membaca sensor gas, mengatur servo, dan logika pemicuan
class SensorAmonia {
  int pin;                  // Pin analog sensor gas
  int batas;                // Ambang batas kadar amonia
  unsigned long jeda;       // Waktu delay setelah servo aktif (milidetik)
  bool terpicu;             // Status apakah servo sedang aktif
  unsigned long terakhirAktif;  // Waktu terakhir servo diaktifkan
  Servo servo;              // Objek servo (mengontrol keran)

public:
  SensorAmonia(int _pin, int _batas, unsigned long _jeda, int pinServo)
    : pin(_pin), batas(_batas), jeda(_jeda), terpicu(false), terakhirAktif(0) {
    servo.setPeriodHertz(50);      // Frekuensi servo (standar PWM untuk servo)
    servo.attach(pinServo);        // Pasang servo ke pin
    servo.write(0);                // Tutup servo saat awal
  }

  // Fungsi untuk membaca nilai analog sensor
  int baca() {
    return analogRead(pin);
  }

  // Mengecek apakah gas melebihi ambang dan aktifkan servo jika perlu
  int cekDanAktifkan() {
    int nilai = baca();
    unsigned long now = millis();

    Serial.print("Amonia: ");
    Serial.println(nilai);

    // Jika belum terpicu dan gas tinggi, aktifkan servo
    if (!terpicu && nilai > batas) {
      servo.write(90);  // Buka keran
      mulaiCooldown();
      Serial.println("!!! TERPICU: Gas tinggi - Servo aktif");
    }

    // Jika waktu sudah lewat, reset servo
    if (terpicu && now - terakhirAktif > jeda) {
      servo.write(0);  // Tutup keran
      terpicu = false;
      Serial.println("RESET: Cooldown selesai - Servo off");
    }

    return nilai;
  }

  void mulaiCooldown() {
    terakhirAktif = millis();
    terpicu = true;
  }


  unsigned long int ambilNilaiCooldownTersisa(){
    unsigned long now = millis();  // Tambahkan ini
    if (now - terakhirAktif > jeda){
      return 0;
    } else {
      return jeda - (now - terakhirAktif);
    }
  }

  // Paksa buka servo dari perintah server
  void paksaBuka() {
    servo.write(90);
    Serial.println("Servo dipaksa buka");
  }

  // Paksa tutup servo dari perintah server
  void paksaTutup() {
    servo.write(0);
    Serial.println("Servo dipaksa tutup");
  }

  // Update ambang batas dari server
  void aturBatas(int b) {
    batas = b;
    Serial.print("Ambang baru: ");
    Serial.println(batas);
  }

  bool isTerpicu() {
  return terpicu;
}

  int getBatas() { return batas; } // Getter ambang jika dibutuhkan
};

// ======== Kelas IoTClient ========
// Bertanggung jawab untuk koneksi WiFi dan komunikasi HTTP
class IoTClient {
public:
  // Menghubungkan ke WiFi
  void connectWifi(const char* ssid, const char* pass) {
    WiFi.begin(ssid, pass);
    Serial.print("Menghubungkan WiFi");
    while (WiFi.status() != WL_CONNECTED) {
      delay(500); Serial.print(".");
    }
    Serial.println("\nWiFi Terhubung");
  }

  // Mengirim status kadar amonia (POST)
  void kirimStatus(int nilai, unsigned long int cooldown_tersisa, bool terpicu) {
    if (WiFi.status() != WL_CONNECTED) return;

    HTTPClient http;
    String url = String(BASE_URL) + endpointStatus;
    http.begin(url);
    http.addHeader("Content-Type", "application/json");

    // Buat JSON body
    StaticJsonDocument<200> doc;
    doc["id_kolam"] = ID_KOLAM;
    doc["nilai_amonia"] = nilai;
    doc["cooldown_tersisa"] = cooldown_tersisa ;  // menggunakan Milisecond
    doc["keran_terbuka"] = terpicu;

    String body;
    serializeJson(doc, body);

    // Kirim POST
    int code = http.POST(body);
    Serial.print("[POST Status] HTTP: ");
    Serial.println(code);
    http.end();
  }


  void kirimStatusPerintah(int id_perintah, int status, char *pesan) {
    if (WiFi.status() != WL_CONNECTED) return;

    HTTPClient http;
    String url = String(BASE_URL) + "/api/iot/1/commands/update-status";
    http.begin(url);
    http.addHeader("Content-Type", "application/json");

    StaticJsonDocument<128> doc;
    doc["id_perintah"] = id_perintah;
    doc["status"] = status;
    doc["pesan"] = pesan;

    String body;
    serializeJson(doc, body);

    int httpCode = http.PUT(body);
    Serial.print("[UPDATE STATUS] HTTP: ");
    Serial.println(httpCode);
    http.end();
  }


  // Mengambil nilai ambang dari server (GET)
  void ambilSetting(SensorAmonia& sensor) {
    if (WiFi.status() != WL_CONNECTED) return;

    HTTPClient http;
    String url = String(BASE_URL) + endpointSettings;
    http.begin(url);
    int code = http.GET();

    if (code == 200) {
      String payload = http.getString();
      StaticJsonDocument<256> doc;
      if (!deserializeJson(doc, payload)) {
        sensor.aturBatas(doc["batasan_amonia"]);
      }
    }
    http.end();
  }

  // Mengambil perintah server untuk kontrol IoT (GET)
  void ambilPerintah(SensorAmonia& sensor) {
    if (WiFi.status() != WL_CONNECTED) return;

    HTTPClient http;
    String url = String(BASE_URL) + endpointCommands;
    http.begin(url);
    int code = http.GET();

    if (code == 200) {
      String payload = http.getString();
      StaticJsonDocument<512> doc;
      if (!deserializeJson(doc, payload)) {
        JsonObject cmd = doc["id_kolam"];
        int tipe = cmd["tipe"];
        int id_perintah = cmd["id"];
        JsonObject data = cmd["data"];

        bool sukses = true;
        char *pesan = "Perintah Sukses";

        switch (tipe) {
          case OPEN_KERAN:
            sensor.paksaBuka();
            sensor.mulaiCooldown();  // Aktifkan timer cooldown
            break;
          case CLOSE_KERAN:
            if (sensor.ambilNilaiCooldownTersisa() == 0){
              sensor.paksaTutup();
            } else {
              sukses = false;
              pesan = "Keran masih dalam cooldown";
            }
            break;
          case UPDATE_BATAS_NH3:
            if (data.containsKey("batas")) {
              sensor.aturBatas(data["batas"]);
            } else {
              sukses = false;
            }
            break;
          default:
            sukses = false;
            Serial.println("Perintah tidak dikenal");
        }

        kirimStatusPerintah(id_perintah, sukses ? SUCCESS : FAILED, pesan);
      }
    }
    http.end();
  }

};

// ======== Objek Global ========
SensorAmonia sensor(34, 600, 60000, 13);  // pin sensor, ambang, delay(ms), pin servo
IoTClient client;                         // pengelola WiFi dan HTTP

// ======== Setup (dijalankan sekali saat boot) ========
void setup() {
  Serial.begin(115200);             // Mulai komunikasi serial
  client.connectWifi(SSID, PASSWORD); // Koneksi ke WiFi
  client.ambilSetting(sensor);     // Ambil konfigurasi awal dari server
}

// ======== Loop utama (berjalan terus) ========
void loop() {
  int nilai = sensor.cekDanAktifkan();  // Baca dan proses sensor
  client.kirimStatus(nilai, sensor.ambilNilaiCooldownTersisa(), sensor.isTerpicu());            // Kirim nilai ke server
  client.ambilPerintah(sensor);         // Ambil perintah dari server
  delay(1000);                          // Delay 1 detik antar siklus
}
