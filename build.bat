@echo off
setlocal
echo ============================================
echo   Smart Nota Portable - Build Script
echo ============================================
echo.

rem -- Cek Python tersedia -------------------------------------------
where py >nul 2>nul
if errorlevel 1 (
  echo GAGAL: Python launcher "py" tidak ditemukan.
  echo Install Python 3.10+ dari https://www.python.org/downloads/
  echo Pastikan centang "Add Python to PATH" saat install.
  echo.
  echo Tekan sembarang tombol untuk menutup...
  pause > nul
  exit /b 1
)

echo [1/5] Install dependencies...
py -m pip install --upgrade pip
py -m pip install -r requirements.txt pyinstaller
if errorlevel 1 (
  echo.
  echo GAGAL install dependencies! Pastikan koneksi internet aktif.
  echo.
  echo Tekan sembarang tombol untuk menutup...
  pause > nul
  exit /b 1
)

echo.
echo [2/5] Tutup SmartNota.exe yang sedang berjalan (jika ada)...
taskkill /IM SmartNota.exe /F >nul 2>nul
if errorlevel 1 (
  echo   Tidak ada proses SmartNota.exe yang berjalan.
) else (
  echo   SmartNota.exe berhasil ditutup.
  timeout /t 1 /nobreak >nul
)

echo.
echo [3/5] Bersihkan build lama (spec + work dir)...
if exist "SmartNota.spec" del /f /q "SmartNota.spec" >nul 2>nul
if exist "build\SmartNota" rmdir /s /q "build\SmartNota" >nul 2>nul

echo.
echo [4/5] Cek asset folder "img"...
if not exist "img" (
  echo   PERINGATAN: Folder "img" tidak ditemukan.
  echo   Logo kop/cap/ttd pada PDF tidak akan tampil.
  echo.
)

echo [5/5] Build .exe...
py -m PyInstaller ^
  --clean ^
  --noconfirm ^
  --onefile ^
  --noconsole ^
  --name "SmartNota" ^
  --add-data "img;img" ^
  --exclude-module matplotlib ^
  --exclude-module numpy ^
  --exclude-module pandas ^
  --exclude-module tkinter ^
  app.py

if errorlevel 1 (
  echo.
  echo GAGAL build! Cek pesan error di atas.
  echo Jika muncul "Access is denied", pastikan SmartNota.exe sudah ditutup
  echo dan folder dist tidak sedang dibuka di File Explorer.
  echo.
  echo Tekan sembarang tombol untuk menutup...
  pause > nul
  exit /b 1
)

echo.
echo ============================================
echo  SELESAI!
echo  File EXE: dist\SmartNota.exe
echo ============================================
echo.
echo  CARA PAKAI:
echo   1. Copy dist\SmartNota.exe ke folder mana saja
echo   2. Double-click SmartNota.exe
echo   3. Browser otomatis terbuka ke localhost:5000
echo   4. Ikon muncul di System Tray kanan bawah
echo.
echo  Tekan sembarang tombol untuk menutup...
pause > nul
endlocal