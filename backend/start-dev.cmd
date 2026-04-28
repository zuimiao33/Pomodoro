@echo off
set "BACKEND_DIR=%~dp0"
cd /d "%BACKEND_DIR%"

netstat -ano | findstr "127.0.0.1:8000" | findstr "LISTENING" >nul
if %errorlevel%==0 (
  echo Backend is already running: http://127.0.0.1:8000
  echo API docs: http://127.0.0.1:8000/docs
  exit /b 0
)

python -m uvicorn app.main:app --app-dir "%BACKEND_DIR%" --host 127.0.0.1 --port 8000
