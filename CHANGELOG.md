# Changelog

Semua perubahan penting pada project ini didokumentasikan di file ini.

## [1.2.0] - 2026-03-10

### Changed
- Sidebar PDF nota (panel kiri + logo kop + info "Tagihan Untuk" + Contact Person) kini tampil di **setiap halaman** PDF, bukan hanya halaman pertama. Berguna saat item nota banyak sehingga nota lebih dari satu halaman.
- `Masukkan Semua via Tambah Barang` kini melakukan **batch insert** ke Preview Nota dalam satu kali render + satu kali autosave (sebelumnya memproses tiap item secara berurutan dengan fetch/render/save per item). Import Excel dengan banyak baris jadi jauh lebih cepat.
- Baris import dengan nama produk sama otomatis **digabung** (qty dijumlahkan) agar tidak dobel di Preview.

### Added
- **Edit Nota** dari halaman Detail: tombol `Edit Nota` membuka panel untuk mengubah nama pelanggan, tanggal nota, dan seluruh item (nama, qty, satuan, keterangan, harga) — termasuk tambah/hapus baris. Total nota dihitung ulang otomatis.
- Endpoint `POST /api/nota/update/<id>` untuk menyimpan perubahan nota (mengganti seluruh item, meng-upsert harga produk, dan menghitung ulang total di server).
- **Restart Server** pada menu System Tray: server dapat di-restart tanpa menutup aplikasi (menggunakan Werkzeug `make_server` + `shutdown()` yang bersih).
- **Single instance dengan ambil-alih**: membuka `SmartNota.exe` saat aplikasi sudah berjalan akan menghentikan instance lama (data tersimpan otomatis di database) lalu menjalankan instance baru dan membuka browser — tidak ada server ganda.
- Endpoint internal `POST /api/shutdown` (hanya dari localhost) untuk meminta instance lama berhenti dengan bersih.
- Selama belum di-*Stop*, aplikasi tetap hidup di system tray dan bisa dibuka kembali kapan saja dari browser.
- **Pagination** pada halaman Daftar Produk: selector jumlah per halaman (10/25/50/100, default 25), info rentang `x–y dari N`, tombol navigasi dengan ellipsis, serta nomor urut (`#`) global yang berlanjut antar halaman.
- Pagination terintegrasi dengan pencarian (filter dulu, lalu dipaginasi) dan menampilkan pesan "tidak ada produk cocok" bila hasil kosong.
- Notifikasi peringatan saat item hasil import memiliki harga `0` (item tetap dimasukkan ke Preview untuk dicek manual).

## [1.1.0] - 2026-03-09

### Added
- Import item dari Excel via endpoint `POST /api/import/excel` dengan parser `openpyxl`.
- Auto-baca metadata `pelanggan` dan `tanggal nota` dari file Excel.
- Queue import (`Daftar Item Import`) untuk review sebelum item dimasukkan ke nota.
- Field `Tanggal Nota` pada form nota + dukungan simpan tanggal custom ke database.
- Format nomor nota baru: `#NNN/OB/SMP/DD/MM/YYYY`.
- Aksi edit nomor nota dari halaman Riwayat via endpoint `POST /api/nota/edit-nomor/<id>`.

### Changed
- Desain PDF dituning agar lebih mirip template referensi (layout, tipografi, posisi elemen).
- Asset PDF (`LOGOKOP`, `LOGOCAP`, `TTD`) di-load otomatis dari folder `img` dengan prioritas file `.png`.
- Proses simpan nota meng-upsert data produk termasuk nama hasil edit agar sinkron dengan daftar produk.
- Build config diperbarui agar folder `img` ikut ter-bundle di executable PyInstaller.

### Fixed
- Matching nama produk saat import dibuat lebih toleran (normalisasi spasi/simbol + fallback contains).
- Alur import disesuaikan agar item dapat dimasukkan via mekanisme `Tambah Barang`, bukan langsung hard insert.
- Kasus harga satuan menjadi `0` di preview diperbaiki dengan fallback ke nilai form + validasi blokir item harga 0.
- Perbaikan stabilitas build dan path asset saat aplikasi dijalankan sebagai `.exe` (frozen runtime).

### Dependencies
- Tambahan dependency: `openpyxl>=3.1`.

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
