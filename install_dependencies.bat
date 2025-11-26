@echo off
echo 🚀 Installing Trading Dashboard Dependencies
echo ==========================================

echo.
echo 📦 Installing Python packages...
python -m pip install --upgrade pip
python -m pip install flask==2.3.3
python -m pip install flask-cors==4.0.0
python -m pip install sqlalchemy==2.0.21
python -m pip install python-dotenv==1.0.0
python -m pip install alembic==1.12.0

if errorlevel 1 (
    echo.
    echo ❌ Installation failed. Trying alternative method...
    py -m pip install flask flask-cors sqlalchemy python-dotenv alembic
)

echo.
echo ✅ Dependencies installed successfully!
echo.
echo 🗄️ Setting up database...
python setup_database.py

if errorlevel 1 (
    echo ❌ Database setup failed
    pause
    exit /b 1
)

echo.
echo ✅ Setup complete! 
echo.
echo 🌐 To start the server, run:
echo    start_full_server.bat
echo.
pause