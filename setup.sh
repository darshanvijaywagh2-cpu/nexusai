#!/bin/bash
# X AI Assistant - One Command Setup
sudo apt update && sudo apt install -y xdotool wmctrl gnome-screenshot playerctl xclip xsel espeak ffmpeg portaudio19-dev libportaudio2 tesseract-ocr redis-server libreoffice imagemagick && pip3 install --break-system-packages fastapi uvicorn psutil pillow openpyxl xlsxwriter gtts pytesseract python-pptx pypdf2 opencv-python speechrecognition pyaudio && echo "DONE! Run: python3 main.py"
