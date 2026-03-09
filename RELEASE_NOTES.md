# 📦 Release Notes

---

## v1.1.0 — Template, Import Excel, dan Stabilitas Build

**Tanggal:** 2026-03-09

### ✅ Highlight Update

- **Template PDF Lebih Presisi** — Layout invoice dituning agar lebih mendekati template referensi.
- **Auto Asset dari Folder `img`** — `LOGOKOP`, `LOGOCAP`, dan `TTD` otomatis dipakai saat generate PDF.
- **Import Excel** — Bisa import multi item dari Excel dengan parsing data lebih toleran.
- **Auto Baca Customer & Tanggal** — Data pelanggan/tanggal dari Excel ikut terisi ke form nota.
- **Import Queue** — Item import masuk antrean dulu untuk direview sebelum dimasukkan ke nota.
- **Nomor Nota Baru** — Format jadi `#NNN/OB/SMP/DD/MM/YYYY`.
- **Edit Nomor dari Riwayat** — Nomor nota bisa diubah dari halaman riwayat dengan validasi duplikasi.
- **Simpan Produk Sinkron** — Nama produk hasil edit di draft ikut di-upsert ke daftar produk.
- **Build EXE Lebih Aman** — Konfigurasi PyInstaller diperbarui agar folder `img` ikut ter-bundle.

### 🛠️ Perbaikan Penting

- Perbaikan kasus **harga satuan = 0** pada flow import -> form -> tambah item.
- Perbaikan logika match nama produk saat import (normalisasi + fallback).
- Perbaikan stabilitas path asset saat app berjalan dalam mode `.exe`.

### 📦 Dependency

- Tambahan: `openpyxl>=3.1`

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
