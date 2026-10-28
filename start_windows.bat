@echo off
setlocal
cd /d "%~dp0"
chcp 65001 >nul
title Wadi Rum Mirage 2.8.0 - Fixed Launch
echo ======================================
echo  WADI RUM MIRAGE 2.8.0 - BILINGUAL
echo ======================================
python -m pip install -r backend\requirements.txt
if errorlevel 1 (echo ERROR: Install failed & pause & exit /b 1)
echo.
echo IMPORTANT: Use the new port 8765 to avoid the old site on port 8000.
echo Open http://127.0.0.1:8765 in Chrome.
echo.
start "" "http://127.0.0.1:8765"
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8765
pause
