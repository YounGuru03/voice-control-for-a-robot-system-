#!/bin/bash
# Linux/Mac installation script for Voice Control System

echo "============================================================"
echo "Voice Control System - Installation Script"
echo "============================================================"
echo ""

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8 or later"
    exit 1
fi

echo "Python detected:"
python3 --version
echo ""

# Create virtual environment (optional but recommended)
echo "Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "WARNING: Failed to create virtual environment"
    echo "Continuing with system Python..."
    PYTHON_CMD="python3"
else
    echo "Virtual environment created successfully"
    source venv/bin/activate
    PYTHON_CMD="python"
fi
echo ""

# Upgrade pip
echo "Upgrading pip..."
$PYTHON_CMD -m pip install --upgrade pip
echo ""

# Install dependencies
echo "Installing dependencies..."
echo "This may take several minutes..."
$PYTHON_CMD -m pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi
echo ""

# Download Whisper model
echo "Downloading Whisper model (base)..."
echo "This will download approximately 150MB"
$PYTHON_CMD -c "import whisper; whisper.load_model('base')"
if [ $? -ne 0 ]; then
    echo "WARNING: Failed to download Whisper model"
    echo "The model will be downloaded on first run"
fi
echo ""

echo "============================================================"
echo "Installation Complete!"
echo "============================================================"
echo ""
echo "To run the system:"
echo "  python main.py"
echo ""
echo "For help:"
echo "  python main.py --help"
echo ""
echo "See README.md and USAGE.md for more information"
echo ""
