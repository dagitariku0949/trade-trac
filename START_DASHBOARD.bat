@echo off
title Trading Dashboard Starter
color 0A

echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║                🚀 TRADING DASHBOARD 🚀                   ║
echo ║                                                          ║
echo ║  This will start your trading dashboard automatically    ║
echo ║  Just wait and your browser will open!                  ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

echo 🔍 Checking system...

REM Try to start with simple server first (no dependencies needed)
echo ✅ Starting simple server (no setup required)...
echo.
echo 🌐 Your dashboard will open at:
echo    http://localhost:8000/admin-standalone.html
echo.
echo 🔥 Features available:
echo    ✅ Admin panel interface
echo    ✅ Dashboard preview
echo    ✅ All styling and design
echo.
echo 📱 Opening browser in 3 seconds...

timeout /t 3 /nobreak >nul

REM Start simple Python server
start /min python simple_server.py

REM Wait a moment for server to start
timeout /t 2 /nobreak >nul

REM Open browser
start http://localhost:8000/admin-standalone.html

echo.
echo ✅ Dashboard opened in your browser!
echo.
echo 🛑 To stop: Close this window or press Ctrl+C
echo.

REM Keep window open
pause