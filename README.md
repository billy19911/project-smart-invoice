# 🧾 Smart Nota Portable

Aplikasi kasir / nota penjualan berbasis web yang berjalan lokal di laptop — bisa diakses dari HP lewat Wi-Fi yang sama.

![Version](https://img.shields.io/badge/version-1.0.0-indigo)
![Platform](https://img.shields.io/badge/platform-Windows-blue)
![Python](https://img.shields.io/badge/python-3.10%2B-yellow)

---

## ✨ Fitur

| Fitur | Keterangan |
|---|---|
| 📋 Input Nota | Buat nota penjualan dengan mudah |
| 🔍 Smart Search | Fuzzy search produk saat ketik nama barang |
| 🏷️ Tiered Pricing | Harga otomatis ganti ke Grosir jika Qty ≥ Min Grosir |
| 🧠 Auto-Learning | Produk baru otomatis tersimpan ke database |
| 💾 Auto-Save Draft | Form tidak hilang saat refresh |
| 📦 Daftar Produk | Lihat, edit, dan hapus produk |
| 🕒 Riwayat Nota | Lihat semua nota + filter pencarian |
| 📄 Export PDF | Download nota dalam format PDF siap cetak |
| 📱 Mobile Friendly | Bisa diakses dari HP lewat Wi-Fi |
| 🖥️ System Tray | Ikon di pojok kanan bawah (taskbar): Buka / Restart Server / Stop Server |

---

## 🚀 Cara Pakai (.exe)

1. Download **SmartNota.exe** dari halaman [Releases](../../releases/latest)
2. Taruh di folder mana saja
3. Double-click `SmartNota.exe`
4. Browser terbuka otomatis ke `http://localhost:5000`
5. Dari HP (pastikan 1 Wi-Fi): buka browser → ketik `http://<IP_LAPTOP>:5000`

> IP laptop akan tampil di sidebar aplikasi secara otomatis.

**Ikon System Tray** (pojok kanan bawah taskbar) — klik kanan untuk:
- 🌐 **Buka Smart Nota** — buka aplikasi di browser
- 🔄 **Restart Server** — restart server tanpa menutup aplikasi
- ⏹ **Stop Server** — matikan server & tutup aplikasi

Selama aplikasi belum di-**Stop**, server tetap hidup di background sehingga
bisa dibuka kapan saja dari browser (`http://localhost:5000`).

> **Buka ulang `SmartNota.exe` saat masih berjalan?** Aplikasi lama otomatis
> dihentikan (data sudah tersimpan di database) lalu instance baru dijalankan
> dan browser dibuka — jadi tidak ada server ganda.

---

## 🛠️ Cara Jalankan dari Source Code

**Install dependencies:**
```bash
py -m pip install -r requirements.txt
```

**Jalankan:**
```bash
py app.py
```

---

## 📦 Cara Build ke .exe

Install dependencies + PyInstaller:
```bash
py -m pip install -r requirements.txt pyinstaller
```

Lalu double-click `build.bat` — atau manual:
```bash
py -m PyInstaller --onefile --noconsole --name "SmartNota" --add-data "img;img" app.py
```

File `.exe` akan muncul di folder `dist/`.

> `--add-data "img;img"` wajib disertakan agar logo kop/cap/ttd ikut terbundle untuk PDF.

---

## 📁 Struktur File

```
Smart Nota Portable/
├── app.py           # Aplikasi utama (Flask + semua HTML embedded)
├── build.bat        # Script build ke .exe
├── requirements.txt # Daftar library
├── img/             # Asset PDF (LOGOKOP, LOGOCAP, TTD)
├── smartnota.db     # Database SQLite (dibuat otomatis saat pertama jalan)
└── .gitignore
```

> Database `smartnota.db` otomatis dibuat di folder yang sama dengan `.exe`.

---

## 🖥️ Tech Stack

- **Backend**: Python + Flask
- **Database**: SQLite
- **PDF**: FPDF2
- **UI**: Bootstrap 5 (CDN) + Bootstrap Icons
- **Tray**: pystray + Pillow
- **Build**: PyInstaller

---

## 👨‍💻 Credits

Design by **bil**
