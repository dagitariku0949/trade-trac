@echo off
echo 🖥️ Creating Desktop Shortcut for Trading Dashboard...

REM Get current directory
set CURRENT_DIR=%~dp0

REM Create VBS script to create shortcut
echo Set oWS = WScript.CreateObject("WScript.Shell"^) > CreateShortcut.vbs
echo sLinkFile = "%USERPROFILE%\Desktop\Trading Dashboard.lnk" >> CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile^) >> CreateShortcut.vbs
echo oLink.TargetPath = "%CURRENT_DIR%SUPER_EASY_START.bat" >> CreateShortcut.vbs
echo oLink.WorkingDirectory = "%CURRENT_DIR%" >> CreateShortcut.vbs
echo oLink.Description = "Trading Dashboard - One Click Start" >> CreateShortcut.vbs
echo oLink.IconLocation = "shell32.dll,21" >> CreateShortcut.vbs
echo oLink.Save >> CreateShortcut.vbs

REM Run the VBS script
cscript CreateShortcut.vbs >nul

REM Clean up
del CreateShortcut.vbs

echo ✅ Desktop shortcut created!
echo.
echo 🎯 Now you can:
echo    1. Double-click "Trading Dashboard" on your desktop
echo    2. Wait for automatic setup
echo    3. Your dashboard will open in browser
echo.
echo 🚀 It's that simple!
pause