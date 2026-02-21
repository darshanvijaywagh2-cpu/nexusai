#!/bin/bash
# One-command setup for X AI Assistant
# Just run this on your desktop!

echo "🤖 Setting up X - AI Assistant"
echo "=============================="

# Install system packages
sudo apt update && sudo apt install -y \
    xdotool \
    wmctrl \
    gnome-screenshot \
    playerctl \
    xclip \
    xsel \
    espeak \
    ffmpeg \
    portaudio19-dev \
    libportaudio2 \
    tesseract-ocr

# Install Python packages
pip3 install --break-system-packages \
    fastapi \
    uvicorn \
    psutil \
    pillow \
    openpyxl \
    xlsxwriter \
    gtts \
    pytesseract \
    python-pptx \
    pypdf2 \
    opencv-python \
    speechrecognition \
    pyaudio

echo ""
echo "✅ DONE!"
echo ""
echo "Now run:"
echo "  python3 main.py"
echo ""
echo "Then connect tunnel:"
echo "  cloudflared tunnel --url http://localhost:8000"
echo ""
echo "🎉 Ready!"
