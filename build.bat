@echo off
echo ============================================
echo   Smart Nota Portable - Build Script
echo ============================================
echo.

echo [1/3] Install dependencies...
py -m pip install flask fpdf2 pystray Pillow pyinstaller openpyxl
if errorlevel 1 (
  echo.
  echo GAGAL install! Pastikan Python sudah terinstall.
  echo.
  echo Tekan sembarang tombol untuk menutup...
  pause > nul
  exit /b 1
)

echo.
echo [2/3] Build .exe...
py -m PyInstaller ^
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
  echo GAGAL build!
  echo.
  echo Tekan sembarang tombol untuk menutup...
  pause > nul
  exit /b 1
)

echo.
echo ============================================
echo  [3/3] SELESAI!
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
