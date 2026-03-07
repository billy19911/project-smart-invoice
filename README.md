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
| 🖥️ System Tray | Ikon di taskbar, klik kanan untuk Stop/Buka |

---

## 🚀 Cara Pakai (.exe)

1. Download **SmartNota.exe** dari halaman [Releases](../../releases/latest)
2. Taruh di folder mana saja
3. Double-click `SmartNota.exe`
4. Browser terbuka otomatis ke `http://localhost:5000`
5. Dari HP (pastikan 1 Wi-Fi): buka browser → ketik `http://<IP_LAPTOP>:5000`

> IP laptop akan tampil di sidebar aplikasi secara otomatis.

---

## 🛠️ Cara Jalankan dari Source Code

**Install dependencies:**
```bash
py -m pip install flask fpdf2 pystray Pillow
```

**Jalankan:**
```bash
py app.py
```

---

## 📦 Cara Build ke .exe

```bash
py -m pip install flask fpdf2 pystray Pillow pyinstaller
```

Lalu double-click `build.bat` — atau manual:

```bash
py -m PyInstaller --onefile --noconsole --name "SmartNota" app.py
```

File `.exe` akan muncul di folder `dist/`.

---

## 📁 Struktur File

```
Smart Nota Portable/
├── app.py           # Aplikasi utama (Flask + semua HTML embedded)
├── build.bat        # Script build ke .exe
├── requirements.txt # Daftar library
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
