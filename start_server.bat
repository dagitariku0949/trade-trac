@echo off
echo 🚀 Starting Trading Dashboard Server...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python from https://python.org
    echo.
    pause
    exit /b 1
)

echo ✅ Python found
echo.

REM Install required packages
echo 📦 Installing required packages...
python -m pip install flask flask-cors sqlalchemy python-dotenv alembic

if errorlevel 1 (
    echo ❌ Failed to install packages
    pause
    exit /b 1
)

echo ✅ Packages installed
echo.

REM Setup database
echo 🗄️ Setting up database...
python setup_database.py

if errorlevel 1 (
    echo ❌ Database setup failed
    pause
    exit /b 1
)

echo ✅ Database ready
echo.

REM Start the server
echo 🌐 Starting server on http://localhost:5000
echo.
echo 📋 Available URLs:
echo   Main Dashboard: http://localhost:5000
echo   Admin Panel:    http://localhost:5000/admin.html
echo.
echo Press Ctrl+C to stop the server
echo.

cd backend
python app.py

pause