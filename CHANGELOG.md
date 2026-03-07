# Changelog

Semua perubahan penting pada project ini didokumentasikan di file ini.

---

## [1.0.0] - 2026-03-07

### 🎉 Initial Release

#### Fitur Utama
- **Dashboard** – Statistik total nota, omzet, produk, nota hari ini
- **Input Nota** – Form input penjualan dengan preview real-time
- **Auto-Learning Produk** – Produk baru otomatis tersimpan ke database saat simpan nota
- **Tiered Pricing** – Harga grosir aktif otomatis berdasarkan qty minimum
- **Smart Search** – Fuzzy search + suggestion dropdown saat input nama barang
- **Auto-Save Draft** – Draft tersimpan di localStorage, tidak hilang saat refresh
- **Riwayat Nota** – Tabel semua nota dengan filter tanggal & pencarian
- **Detail Nota** – Tampilan nota lengkap siap print
- **Export PDF** – Generate PDF dengan kop surat, tabel item, total, tanda tangan
- **Daftar Produk** – Lihat, edit, dan hapus produk dari database
- **System Tray** – Ikon di taskbar kanan bawah (Buka / Stop Server)
- **Auto Browser** – Browser otomatis terbuka saat .exe dijalankan
- **Akses dari HP** – Server berjalan di `0.0.0.0:5000`, IP ditampilkan di sidebar
- **Single File EXE** – Semua template HTML embedded di `app.py`, build `--onefile`

#### Tech Stack
- Python 3.10+
- Flask 2.3+
- FPDF2 2.7+
- pystray 0.19+
- Pillow 10+
- PyInstaller 6+
- Bootstrap 5.3 (CDN)
- Bootstrap Icons 1.11 (CDN)
- SQLite (database lokal)
