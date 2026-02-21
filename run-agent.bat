@echo off
REM X AI Desktop Agent - Windows Quick Setup

echo.
echo ========================================
echo   X AI Desktop Agent - Quick Setup
echo ========================================
echo.

echo [1/4] Downloading agent...
curl -s -o agent.py https://raw.githubusercontent.com/darshanvijaywagh2-cpu/nexusai/main/server/agent.py
echo [1/4] Done!

echo [2/4] Installing Python packages...
pip install requests fastapi uvicorn pillow >nul 2>&1
echo [2/4] Done!

echo [3/4] Setting VPS URL...
set VPS_URL=https://superintendent-info-smooth-gordon.trycloudflare.com
echo [3/4] Done!

echo.
echo ========================================
echo   Starting X Agent...
echo ========================================
echo.

REM Start agent
python agent.py

pause
