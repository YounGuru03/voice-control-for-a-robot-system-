@echo off
REM Windows installation script for Voice Control System

echo ============================================================
echo Voice Control System - Installation Script
echo ============================================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or later from https://www.python.org/
    pause
    exit /b 1
)

echo Python detected:
python --version
echo.

REM Create virtual environment (optional but recommended)
echo Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo WARNING: Failed to create virtual environment
    echo Continuing with system Python...
) else (
    echo Virtual environment created successfully
    call venv\Scripts\activate.bat
)
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip
echo.

REM Install dependencies
echo Installing dependencies...
echo This may take several minutes...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo.

REM Download Whisper model
echo Downloading Whisper model (base)...
echo This will download approximately 150MB
python -c "import whisper; whisper.load_model('base')"
if errorlevel 1 (
    echo WARNING: Failed to download Whisper model
    echo The model will be downloaded on first run
)
echo.

echo ============================================================
echo Installation Complete!
echo ============================================================
echo.
echo To run the system:
echo   python main.py
echo.
echo For help:
echo   python main.py --help
echo.
echo See README.md and USAGE.md for more information
echo.
pause
