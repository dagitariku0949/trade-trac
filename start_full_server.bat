@echo off
echo 🚀 Starting Full Trading Dashboard Server
echo =========================================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please run install_dependencies.bat first
    echo.
    pause
    exit /b 1
)

echo ✅ Python found: 
python --version
echo.

REM Check if Flask is installed
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo ❌ Flask not installed. Running dependency installation...
    call install_dependencies.bat
)

echo ✅ Dependencies ready
echo.

REM Setup database if it doesn't exist
if not exist "database.db" (
    echo 🗄️ Setting up database...
    python setup_database.py
)

echo ✅ Database ready
echo.

REM Start the full backend server
echo 🌐 Starting Flask backend server...
echo.
echo 📋 Server will be available at:
echo   Main Dashboard: http://localhost:5000
echo   Admin Panel:    http://localhost:5000/admin.html
echo.
echo 🔥 Full functionality enabled:
echo   ✅ Real-time data
echo   ✅ Database operations
echo   ✅ Account management
echo   ✅ Strategy tracking
echo   ✅ Trade management
echo   ✅ Analytics & reports
echo.
echo Press Ctrl+C to stop the server
echo =========================================

cd backend
python app.py

echo.
echo Server stopped.
pause