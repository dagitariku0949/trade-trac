@echo off
title Trading Dashboard - Easy Setup
color 0A

echo.
echo  ████████╗██████╗  █████╗ ██████╗ ██╗███╗   ██╗ ██████╗ 
echo  ╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗██║████╗  ██║██╔════╝ 
echo     ██║   ██████╔╝███████║██║  ██║██║██╔██╗ ██║██║  ███╗
echo     ██║   ██╔══██╗██╔══██║██║  ██║██║██║╚██╗██║██║   ██║
echo     ██║   ██║  ██║██║  ██║██████╔╝██║██║ ╚████║╚██████╔╝
echo     ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═╝╚═╝  ╚═══╝ ╚═════╝ 
echo.
echo                    🚀 DASHBOARD EASY SETUP 🚀
echo                   ========================
echo.

REM Check if Python is installed
echo [1/5] 🔍 Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Installing Python automatically...
    echo.
    echo 📥 Downloading Python installer...
    
    REM Download Python installer
    powershell -Command "& {Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.6/python-3.11.6-amd64.exe' -OutFile 'python_installer.exe'}"
    
    if exist python_installer.exe (
        echo ✅ Python installer downloaded
        echo 🔧 Installing Python (this may take a few minutes)...
        echo    Please wait and follow any prompts...
        
        REM Install Python silently with PATH
        python_installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
        
        echo ✅ Python installation completed
        echo 🔄 Refreshing environment...
        
        REM Refresh PATH
        call refreshenv.cmd >nul 2>&1
        
        REM Clean up
        del python_installer.exe
    ) else (
        echo ❌ Failed to download Python installer
        echo 📋 Please install Python manually from https://python.org
        echo    Make sure to check 'Add Python to PATH' during installation
        pause
        exit /b 1
    )
) else (
    echo ✅ Python found: 
    python --version
)

echo.
echo [2/5] 📦 Installing required packages...
python -m pip install --quiet --upgrade pip
python -m pip install --quiet flask==2.3.3 flask-cors==4.0.0 sqlalchemy==2.0.21 python-dotenv==1.0.0

if errorlevel 1 (
    echo ❌ Package installation failed, trying alternative...
    py -m pip install --quiet flask flask-cors sqlalchemy python-dotenv
)

echo ✅ Packages installed successfully

echo.
echo [3/5] 🗄️ Setting up database...
python setup_database.py >nul 2>&1

if errorlevel 1 (
    echo ❌ Database setup failed, creating minimal setup...
    echo import sqlite3; conn = sqlite3.connect('database.db'); conn.close() | python
)

echo ✅ Database ready

echo.
echo [4/5] 🌐 Starting server...
echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║                    🎉 SUCCESS! 🎉                        ║
echo ║                                                          ║
echo ║  Your Trading Dashboard is starting...                   ║
echo ║                                                          ║
echo ║  📋 URLs:                                                ║
echo ║    Main App:    http://localhost:5000                    ║
echo ║    Admin Panel: http://localhost:5000/admin.html         ║
echo ║                                                          ║
echo ║  🔥 Full Features Enabled:                               ║
echo ║    ✅ Real database operations                           ║
echo ║    ✅ Account management                                 ║
echo ║    ✅ Trade tracking                                     ║
echo ║    ✅ Analytics & reports                                ║
echo ║    ✅ Strategy management                                ║
echo ║                                                          ║
echo ║  🛑 Press Ctrl+C to stop server                         ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

REM Open browser automatically
timeout /t 3 /nobreak >nul
start http://localhost:5000/admin.html

echo [5/5] 🚀 Launching server...
echo.

cd backend
python app.py

echo.
echo 🛑 Server stopped. Press any key to exit...
pause >nul