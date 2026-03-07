# 📦 Release Notes

---

## v1.0.0 — Initial Release

**Tanggal:** 2026-03-07

### ✅ Fitur yang Tersedia

- **Dashboard** — Statistik total nota, omzet, produk, dan nota hari ini
- **Input Nota** — Form input nota dengan preview real-time
- **Smart Search** — Fuzzy/contains search produk saat ketik nama barang
- **Tiered Pricing** — Harga otomatis Retail/Grosir berdasarkan Qty
- **Auto-Learning Produk** — Produk baru tersimpan otomatis ke database
- **Auto-Save Draft** — Form tidak hilang saat refresh (localStorage)
- **Riwayat Nota** — Daftar semua nota + search + filter tanggal
- **Detail Nota** — Tampilan nota lengkap siap print
- **Export PDF** — Download nota PDF dengan kop surat & tanda tangan
- **Daftar Produk** — Lihat, edit, dan hapus produk
- **System Tray** — Ikon di taskbar kanan bawah (Buka/Stop server)
- **Auto Buka Browser** — Browser terbuka otomatis saat .exe dijalankan
- **Akses HP** — IP lokal tampil di sidebar, bisa diakses dari HP via Wi-Fi
- **Single File EXE** — Satu file `.exe`, tidak perlu install apapun

### 📥 Download

| File | Keterangan |
|---|---|
| `SmartNota.exe` | Aplikasi siap pakai (Windows) |

### 💻 Sistem yang Didukung

- Windows 10 / 11 (64-bit)
- Tidak perlu install Python

### 📝 Catatan

- Database `smartnota.db` dibuat otomatis di folder yang sama dengan `.exe`
- Tidak perlu koneksi internet (UI menggunakan Bootstrap CDN — butuh internet untuk tampilan)
