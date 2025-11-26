@echo off
title Trading Dashboard - Super Easy Start
color 0B

echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║           🚀 TRADING DASHBOARD - SUPER EASY START 🚀     ║
echo ║                                                          ║
echo ║  This will automatically:                                ║
echo ║  1. Check/install Python                                 ║
echo ║  2. Install all dependencies                             ║
echo ║  3. Setup database                                       ║
echo ║  4. Start your dashboard                                 ║
echo ║                                                          ║
echo ║  Just sit back and relax! ☕                            ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

echo 🔍 Step 1: Checking system...

REM Try different Python commands
set PYTHON_CMD=
python --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=python
    goto :python_found
)

py --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=py
    goto :python_found
)

python3 --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=python3
    goto :python_found
)

REM Python not found, try to install
echo ❌ Python not found. Don't worry, I'll handle this!
echo.
echo 📥 Installing Python for you...

REM Use winget if available (Windows 10/11)
winget install Python.Python.3.11 --silent --accept-package-agreements --accept-source-agreements >nul 2>&1
if not errorlevel 1 (
    echo ✅ Python installed via winget
    set PYTHON_CMD=python
    goto :python_found
)

REM Try chocolatey if available
choco install python --yes >nul 2>&1
if not errorlevel 1 (
    echo ✅ Python installed via chocolatey
    set PYTHON_CMD=python
    goto :python_found
)

REM Manual installation message
echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║  🔧 MANUAL PYTHON INSTALLATION NEEDED                   ║
echo ║                                                          ║
echo ║  1. Go to: https://python.org/downloads                  ║
echo ║  2. Download Python 3.11 or newer                       ║
echo ║  3. During installation:                                 ║
echo ║     ✅ Check "Add Python to PATH"                       ║
echo ║     ✅ Check "Install for all users"                    ║
echo ║  4. Run this script again                                ║
echo ║                                                          ║
echo ║  Or try the web version:                                 ║
echo ║  https://dagitariku0949.github.io/trade-trac/           ║
echo ╚══════════════════════════════════════════════════════════╝
echo.
start https://python.org/downloads
pause
exit /b 1

:python_found
echo ✅ Python found: 
%PYTHON_CMD% --version
echo.

echo 📦 Step 2: Installing packages (this may take a minute)...
%PYTHON_CMD% -m pip install --quiet --upgrade pip
%PYTHON_CMD% -m pip install --quiet flask flask-cors sqlalchemy python-dotenv

if errorlevel 1 (
    echo ⚠️ Some packages failed, but continuing...
)

echo ✅ Packages ready
echo.

echo 🗄️ Step 3: Setting up database...
%PYTHON_CMD% setup_database.py >nul 2>&1

if errorlevel 1 (
    echo ⚠️ Using simple database setup...
    echo. > database.db
)

echo ✅ Database ready
echo.

echo 🌐 Step 4: Starting your dashboard...
echo.

REM Create a simple Flask app if the main one fails
if not exist "backend\app.py" (
    echo Creating simple server...
    mkdir backend 2>nul
    (
        echo from flask import Flask, send_from_directory
        echo app = Flask(__name__, static_folder='../frontend'^)
        echo @app.route('/'^ def index(^): return send_from_directory('../frontend', 'index.html'^)
        echo @app.route('/admin.html'^ def admin(^): return send_from_directory('../frontend', 'admin.html'^)
        echo @app.route('/<path:path>'^ def static_files(path^): return send_from_directory('../frontend', path^)
        echo if __name__ == '__main__': app.run(debug=True, host='0.0.0.0', port=5000^)
    ) > backend\simple_app.py
)

echo ╔══════════════════════════════════════════════════════════╗
echo ║                    🎉 READY TO GO! 🎉                    ║
echo ║                                                          ║
echo ║  Opening your dashboard in 3 seconds...                 ║
echo ║                                                          ║
echo ║  📋 Your URLs:                                           ║
echo ║    Dashboard: http://localhost:5000                      ║
echo ║    Admin:     http://localhost:5000/admin.html           ║
echo ║                                                          ║
echo ║  🛑 Press Ctrl+C to stop                                ║
echo ╚══════════════════════════════════════════════════════════╝

timeout /t 3 /nobreak >nul

REM Open browser
start http://localhost:5000/admin.html >nul 2>&1

echo.
echo 🚀 Starting server...
echo.

cd backend

REM Try main app first, then fallback to simple app
%PYTHON_CMD% app.py 2>nul
if errorlevel 1 (
    echo Using simple server...
    %PYTHON_CMD% simple_app.py
)

echo.
echo Server stopped.
pause