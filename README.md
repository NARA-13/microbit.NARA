# ICONNECT — micro:bit Control Center

> Control center berbasis browser untuk **BBC micro:bit** melalui **Web Bluetooth (BLE UART)** — lengkap dengan mode **AI Teachable Micro:Bit**: kamera + model AI Teachable Machine yang mengendalikan robot secara real-time.

[![Single File](https://img.shields.io/badge/size-single--file-0D80F2)]() [![No Build](https://img.shields.io/badge/build-none-success)]() [![No Backend](https://img.shields.io/badge/backend-none-success)]() [![i18n](https://img.shields.io/badge/bahasa-5-7C5CFF)]()

Satu file — `index.html` — tanpa build step, tanpa dependensi yang harus diinstal, tanpa backend. Semua pengolahan (kamera, AI, koneksi Bluetooth) terjadi **lokal di browser**.

---

## 📋 Daftar Mode

| # | Mode | Fungsi |
|---|------|--------|
| 01 | **Sensor Preview** | Pantau suhu, kelembaban, cahaya, dan data sensor lain lewat grafik real-time |
| 02 | **Robot Controller** | D-Pad presisi, slider servo, tombol A/B untuk mengemudikan robot |
| 03 | **All Preview** | Semua panel sekaligus: sensor, kontrol robot, dan matriks LED 5×5 |
| 04 | **AI Teachable Micro:Bit** ⭐ | Kamera + AI image classification (Teachable Machine) → command robot via Bluetooth UART |

Tambahan lintas mode: **Command Protocol Configurator** (preset Yahboom Tiny:bit, Standard, Indo, dll.), **block programmer**, log UART, 5 bahasa, 7 skin tema (termasuk *hacker* yang tetap monospace).

---

## 🚀 Memulai

### Persyaratan

| | |
|---|---|
| **Browser** | Chrome / Edge (desktop **atau Android**) — satu-satunya yang mendukung Web Bluetooth |
| **Koneksi** | HTTPS atau `localhost` (wajib untuk kamera & Web Bluetooth) |
| **Hardware** | BBC micro:bit V1/V2 dengan program *Bluetooth UART* ter-flash (untuk mode robot/AI) |
| **Tidak didukung** | Firefox, iOS Safari (Web Bluetooth tidak tersedia) |

### Menjalankan

```bash
# Opsi A — buka langsung
# Double-click index.html di Chrome/Edge.

# Opsi B — server lokal (disarankan untuk kamera + Bluetooth)
python3 -m http.server 8000
# lalu buka http://localhost:8000
```

Atau host ke layanan HTTPS apa pun (GitHub Pages, Netlify, Vercel) untuk pemakaian dari HP.

---

## 🤖 Mode AI Teachable Micro:Bit

```
Camera → AI Model → Command → Bluetooth → Micro:Bit → Robot
```

Fitur: preview kamera live, klasifikasi real-time dengan confidence bar per class, threshold minimum (default **70%**), command mapping yang bisa diubah, monitor log UART langsung, D-Pad manual (backup), visualizer robot 2D, sistem *safety* otomatis STOP, dan **Demo Mode** untuk mencoba tanpa micro:bit.

### 1 · Siapkan model AI (Teachable Machine)

1. Buka [teachablemachine.withgoogle.com](https://teachablemachine.withgoogle.com) → **Image Project**.
2. Buat class, disarankan: `FORWARD`, `BACKWARD`, `LEFT`, `RIGHT`, `STOP` (nama class bebas — bisa gesture, objek, atau kartu gambar).
3. **Export Model** → **Upload (Cloud)** → salin URL yang berakhiran `/`.
4. Tempel di panel *Model AI* → **Load AI Model** → status berubah menjadi **Ready**.

> Class apa pun yang tidak ada di mapping otomatis dipetakan ke `STOP`.

### 2 · Siapkan micro:bit (Bluetooth UART)

Flash program ini via [MakeCode](https://makecode.microbit.org) (extension **Bluetooth**), lalu di **Project Settings** pilih **No Pairing Required** sebelum flash agar browser bisa terhubung tanpa pairing:

```js
bluetooth.startUartService()
bluetooth.onUartDataReceived(delimiters(NewLine), function () {
    let cmd = bluetooth.uartReadUntil(delimiters(NewLine)).trim()
    if (cmd == "FORWARD") {
        // TODO: motor maju (sesuaikan driver robotmu)
    } else if (cmd == "BACKWARD") {
        // TODO: motor mundur
    } else if (cmd == "LEFT") {
        // TODO: belok kiri
    } else if (cmd == "RIGHT") {
        // TODO: belok kanan
    } else if (cmd == "STOP") {
        // TODO: berhenti
    }
})
```

### 3 · Hubungkan & jalankan

1. **Start Kamera** → izinkan akses kamera.
2. **Load AI Model** dengan URL dari langkah 1.
3. **Connect Micro:Bit** → pilih perangkat `BBC micro:bit` di dialog browser.
4. Pilih **AI Mode**, arahkan kamera ke gesture/objek.
5. Pantau semua aktivitas di **Live Command Monitor**:

```
[08:42:01] AI detected: LEFT (94%)
[08:42:01] Sending: LEFT
[08:42:01] Bluetooth: Sent successfully
```

### Format perintah UART

Setiap command dikirim sebagai teks + newline (`\n`) melalui Nordic UART Service:

| Command | Arti |
|---------|------|
| `FORWARD\n` | Maju |
| `BACKWARD\n` | Mundur |
| `LEFT\n` | Belok kiri |
| `RIGHT\n` | Belok kanan |
| `STOP\n` | Berhenti |

### Command Mapping

Class AI dipetakan ke command micro:bit lewat panel *Command Mapping* (default 1:1). Klik **Save Mapping** untuk menyimpan ke LocalStorage. Perubahan select langsung aktif tanpa perlu simpan; tombol simpan memastikan tidak hilang saat browser ditutup.

### Sistem Keamanan (Safety)

Command otomatis menjadi **STOP** ketika:

- kamera mati / izin kamera dicabut
- model AI error (3 kegagalan prediksi berturut-turut)
- confidence di bawah threshold → command **tidak dikirim**, robot di-*hold* STOP
- Bluetooth terputus (muncul warning + toast)
- tidak ada sinyal deteksi selama beberapa detik (watchdog)
- pengguna pindah ke **Manual Mode** (AI dilarang mengontrol)

Anti-spam Bluetooth: command hanya dikirim **saat berubah** + *keep-alive* berkala untuk command gerak; `STOP` tidak pernah diulang terus-menerus.

### Demo Mode

Tombol **Coba Demo Tanpa Micro:Bit** mengaktifkan simulasi deteksi sehingga prediction bar, monitor, dan visualizer robot tetap bergerak — cocok untuk uji UI tanpa hardware. Status **Demo Mode** ditampilkan di bar status. Demo berhenti otomatis saat micro:bit asli terhubung.

---

## ⚙️ Pengaturan

Tersimpan otomatis di LocalStorage (`iconnect.ai.tm`):

| Pengaturan | Default | Rentang | Keterangan |
|------------|---------|---------|------------|
| Minimum confidence | 70% | 50–95% | Di bawah nilai ini command tidak dikirim → STOP |
| AI detection interval | 250 ms | 100–1000 ms | Jeda antar prediksi model |
| Command delay | 350 ms | 0–2000 ms | Jeda minimum antar pengiriman command |
| Keep-alive repeat | 1500 ms | 0–5000 ms | Ulang command gerak berkala (0 = mati) |
| Resolusi kamera | 640×480 | 320×240 – 1920×1080 | Makin rendah makin cepat inferensi |
| Auto-reconnect Bluetooth | ON | — | Sambung ulang otomatis (tanpa dialog) saat koneksi terputus |
| Tema | Dark | Dark/Light | Mengikuti tema global situs |
| URL model & mapping | — | — | Ikut tersimpan otomatis |

---

## 🏗️ Arsitektur Kode

Semua logika mode AI berada dalam satu modul IIFE `ATM` yang terbagi jelas — siap diekstrak ke file terpisah (`src/*.js`) jika ingin multi-file:

| Modul | Peran |
|-------|-------|
| `storage.js` → `Store` | Muat/simpan pengaturan + mapping ke LocalStorage |
| `camera.js` → `Camera` | Siklus hidup `getUserMedia`: start/stop/restart, mirror, stream dihentikan saat halaman ditutup |
| `teachable-machine.js` → `TM` | Muat pustaka TF.js + model TM, cache anti-load-berkali-kali, prediksi frame video |
| `bluetooth.js` → `BLE` | Web Bluetooth: requestDevice (filter `BBC micro:bit`), GATT → Nordic UART (`6e400001-…`), write/notify, auto-reconnect |
| `commands.js` → `Commands` | Mapping class→command, threshold, anti-spam, mode AI/Manual, safety STOP |
| `visualizer.js` → `Viz` | Animasi robot 2D top-down sesuai command aktif (jejak lintasan, pantulan tepi) |
| `Bus` | Event bus kecil (`state`, `preds`, `cmd`, `bleup`, `bledown`, `rx`, …) agar modul decoupled |
| `Mon` | Live Command Monitor (timestamp, auto scroll, clear) |
| `Demo` | Simulasi deteksi tanpa hardware |

Modul ini menempel ke helper host halaman: `$`, `T()` (i18n), `toast()`, `sfx()`, `prefs`, `setTheme()`, `setLang()`.

### Mengembangkan untuk robot lain

- **Ganti platform**: `BLE` adalah satu-satunya modul yang bergantung pada micro:bit. Buat adaptor dengan antarmuka yang sama (`connect`, `disconnect`, `send`, `connected`) dan daftarkan ke `Commands`.
- **Tambah command**: tambahkan ke `DEFAULT_COMMANDS` di `commands.js`, lalu mapping baru otomatis muncul di panel *Command Mapping*.
- **Robot non-gerak**: class AI apa pun yang tidak dikenali mapping aman — jatuh ke `STOP`.

---

## 💾 Penyimpanan Data (LocalStorage)

| Key | Isi |
|-----|-----|
| `iconnect.prefs` | Preferensi global: tema, skin, bahasa, demo, SFX |
| `iconnect.ai.tm` | Pengaturan mode AI: URL model, threshold, interval, delay, keep-alive, resolusi, auto-reconnect, mode, mapping |
| `iconnect_robot_cfg` | Konfigurasi protokol robot (preset command D-Pad) |

Tidak ada data yang dikirim ke server mana pun. **Frame kamera diproses sepenuhnya di dalam browser** oleh model TensorFlow.js — tidak ada upload gambar.

---

## 🌐 Internasionalisasi

Seluruh UI (termasuk mode AI dan semua pesan error) tersedia dalam **5 bahasa**: 🇮🇩 Indonesia · 🇬🇧 English · 🇯🇵 日本語 · 🇨🇳 中文 · 🇪🇸 Español — ganti lewat menu bahasa; teks mengikuti secara langsung.

## 🎨 Tema & Skin

Dark (default) / Light, dan 7 skin: `default`, `glass`, `hacker` (monospace terminal, tidak diubah ke font Apple), `overcomplex`, `ethereal`, `oversimple`, `meme`. Mode AI otomatis mengikuti skin aktif.

## 📱 Responsif

- **Desktop/laptop**: kiri (kamera, manual, visualizer) — kanan (model, Bluetooth, mapping, pengaturan)
- **Tablet**: 2 kolom kartu mode
- **Smartphone**: kamera jadi panel utama, kontrol di bawahnya, tombol D-Pad diperbesar (~74px) agar nyaman saat HP dipasang di atas robot

---

## 🛠️ Troubleshooting

| Masalah | Solusi |
|---------|--------|
| *"Camera permission denied."* | Klik ikon kamera di address bar → izinkan; pastikan halaman HTTPS/localhost |
| *"Your browser does not support Web Bluetooth."* | Gunakan Chrome/Edge; di iPhone belum didukung |
| *"Micro:Bit connection failed."* | Pastikan program Bluetooth UART sudah ter-flash, board tidak sedang terhubung ke app lain, dan **No Pairing Required** aktif |
| *"AI model failed to load."* | URL harus berakhir `/` dan mengarah ke root model (`model.json` + `metadata.json`); model yang di-host sendiri wajib mengizinkan CORS |
| Koneksi sering terputus | Jauhkan dari perangkat 2.4GHz lain; aktifkan **Auto-reconnect**; tutup tab lain yang memakai Bluetooth |
| Command tidak terkirim ke board | Periksa monitor: jika ada `Micro:Bit belum terhubung…`, hubungkan board atau aktifkan Demo Mode untuk uji visual |
| Robot tidak berhenti | Turunkan *Keep-alive repeat*, naikkan threshold, atau tekan STOP di D-Pad (selalu diprioritaskan) |

---

## 👤 Developer

**Nararya Irsyad Kelana** — Developer & UI Designer.
ICONNECT dibangun dari nol: antarmuka bersih, dua tema, dan koneksi Bluetooth Low Energy langsung dari browser tanpa instalasi.

### Kredit

- [Teachable Machine](https://teachablemachine.withgoogle.com) by Google — model image classification
- [TensorFlow.js](https://www.tensorflow.org/js) — inferensi di browser
- [Nordic UART Service](https://docs.nordicsemi.com/bundle/ug_serial_ble/page/UUIDs.html) — profil BLE UART
- [BBC micro:bit](https://microbit.org) & [MakeCode](https://makecode.microbit.org)
- Konsep alur: *Teachable Micro:Bit* (LOFI Robot)
