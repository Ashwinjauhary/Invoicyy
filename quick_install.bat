@echo off
echo 🧾 Invoice Maker - Quick Installer for Windows
echo =====================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python first.
    echo 📥 Download from: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo ✅ Python detected
echo.

REM Install dependencies
echo 📦 Installing dependencies...
python -m pip install --upgrade pip
python -m pip install streamlit pandas plotly reportlab pillow qrcode[pil] requests

if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo ✅ Dependencies installed successfully
echo.

REM Create desktop shortcut
echo 🚀 Creating desktop shortcut...
set DESKTOP=%USERPROFILE%\Desktop
set SCRIPT_PATH=%~dp0web_app.py
set PYTHON_PATH=python

powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%DESKTOP%\Invoice Maker.lnk'); $Shortcut.TargetPath = '%PYTHON_PATH%'; $Shortcut.Arguments = '%SCRIPT_PATH%'; $Shortcut.WorkingDirectory = '%~dp0'; $Shortcut.Description = 'Invoice Maker - Professional Billing System'; $Shortcut.Save()"

echo ✅ Desktop shortcut created
echo.

REM Create start menu shortcut
echo 📱 Creating Start Menu shortcut...
set STARTMENU=%APPDATA%\Microsoft\Windows\Start Menu\Programs
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%STARTMENU%\Invoice Maker.lnk'); $Shortcut.TargetPath = '%PYTHON_PATH%'; $Shortcut.Arguments = '%SCRIPT_PATH%'; $Shortcut.WorkingDirectory = '%~dp0'; $Shortcut.Description = 'Invoice Maker - Professional Billing System'; $Shortcut.Save()"

echo ✅ Start Menu shortcut created
echo.

echo 🎉 Installation completed successfully!
echo.
echo 🚀 Launch Invoice Maker:
echo    • Double-click "Invoice Maker" on desktop
echo    • Search "Invoice Maker" in Start Menu
echo    • Run: python web_app.py
echo.
echo 📱 Invoice Maker will open in your browser!
echo.

REM Ask to launch
set /p LAUNCH="🚀 Launch Invoice Maker now? (y/n): "
if /i "%LAUNCH%"=="y" (
    echo 🌐 Starting Invoice Maker...
    start http://localhost:8501
    python web_app.py
) else (
    echo 👋 Installation complete! Launch Invoice Maker from desktop or Start Menu.
)

pause
