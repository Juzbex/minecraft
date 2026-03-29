#!/bin/bash

echo "========================================"
echo "  Minecraft Clone - Installing Libraries"
echo "========================================"
echo ""

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 is not installed"
    echo "Please install Python3 first"
    exit 1
fi

echo "Python found: $(python3 --version)"
echo ""

echo "Installing required libraries..."
echo "- Installing pygame..."
pip3 install pygame --quiet || pip3 install pygame --user --quiet

echo "- Installing PyOpenGL..."
pip3 install PyOpenGL --quiet || pip3 install PyOpenGL --user --quiet

echo "- Installing numpy..."
pip3 install numpy --quiet || pip3 install numpy --user --quiet

echo ""
echo "========================================"
echo "  Installation Complete!"
echo "========================================"
echo ""
echo "Starting Minecraft Clone..."
echo ""

cd "$(dirname "$0")"
python3 src/minecraft.py

if [ $? -ne 0 ]; then
    echo ""
    echo "The game encountered an error."
    echo "Make sure you have OpenGL drivers installed."
fi
