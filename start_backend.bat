@echo off
title TerraWatch Backend (FastAPI)
cd /d "%~dp0EARLY WARNING AND LAND SLIDE RISK MONITORING SYSTEM IN NER"
call .\.venv\Scripts\activate.bat
python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
pause
