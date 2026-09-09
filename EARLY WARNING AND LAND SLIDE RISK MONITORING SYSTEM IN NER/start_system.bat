@echo off
title TerraWatch Launcher
cd /d "%~dp0"
echo ========================================================
echo Starting TerraWatch AI Landslide Early Warning System
echo ========================================================
echo Starting Backend on http://127.0.0.1:8000 ...
start "TerraWatch Backend" cmd /k "call start_backend.bat"
timeout /t 2 /nobreak >nul
echo Starting Frontend on http://localhost:5173 ...
start "TerraWatch Frontend" cmd /k "call start_frontend.bat"
echo.
echo Both services started!
echo Frontend: http://localhost:5173
echo Backend API Docs: http://127.0.0.1:8000/docs
echo ========================================================
