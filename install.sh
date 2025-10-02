#!/bin/bash

# Installation script for SVG Downloader

set -e

echo "========================================"
echo "SVG Downloader - Installation Script"
echo "========================================"
echo ""

# Check Python version
echo "Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    echo "Please install Python 3.7 or higher from https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✓ Python $PYTHON_VERSION found"
echo ""

# Install Python dependencies
echo "Installing Python dependencies..."
if pip3 install -r requirements.txt; then
    echo "✓ Python dependencies installed"
else
    echo "❌ Failed to install Python dependencies"
    exit 1
fi
echo ""

# Install Playwright browser
echo "Installing Playwright Chromium browser..."
echo "This may take a few minutes..."
if playwright install chromium; then
    echo "✓ Playwright browser installed"
else
    echo "⚠ Playwright browser installation had issues"
    echo "Trying to install system dependencies first..."
    
    # Try with deps on Linux
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "Attempting to install system dependencies (may require sudo)..."
        sudo playwright install-deps chromium || true
        playwright install chromium || true
    fi
fi
echo ""

# Run tests
echo "Running verification tests..."
if python3 test_structure.py; then
    echo "✓ All tests passed"
else
    echo "⚠ Some tests failed, but you may still be able to use the tool"
fi
echo ""

echo "========================================"
echo "Installation Complete!"
echo "========================================"
echo ""
echo "To get started, run:"
echo "  python3 main.py --help"
echo ""
echo "Or see QUICKSTART.md for more information"
echo ""
