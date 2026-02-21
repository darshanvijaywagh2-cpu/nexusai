#!/bin/bash
# X AI Assistant - Complete Desktop Setup
# Run this and everything will be configured automatically

set -e

echo "🤖 Setting up X AI Assistant..."
echo "================================"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
   echo -e "${YELLOW}Please run as sudo${NC}"
   exit 1
fi

echo -e "${GREEN}1. Updating system...${NC}"
apt update && apt upgrade -y

echo -e "${GREEN}2. Installing system packages...${NC}"
apt install -y \
    xdotool \
    wmctrl \
    x11-utils \
    x11-xserver-utils \
    gnome-screenshot \
    gnome-terminal \
    playerctl \
    xclip \
    xsel \
    redis-server \
    libreoffice \
    imagemagick \
    espeak \
    ffmpeg \
    portaudio19-dev \
    libportaudio2 \
    tesseract-ocr

echo -e "${GREEN}3. Installing Python packages...${NC}"
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

echo -e "${GREEN}4. Creating startup script...${NC}"
cat > /usr/local/bin/x-assistant << 'XEOF'
#!/bin/bash
cd /root/nexusai 2>/dev/null || cd ~/nexusai
python3 main.py
XEOF
chmod +x /usr/local/bin/x-assistant

echo -e "${GREEN}5. Creating service...${NC}"
cat > /etc/systemd/system/x-assistant.service << 'SEOF'
[Unit]
Description=X AI Assistant
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/nexusai
ExecStart=/usr/bin/python3 /root/nexusai/main.py
Restart=always

[Install]
WantedBy=multi-user.target
SEOF

systemctl daemon-reload
systemctl enable x-assistant

echo ""
echo -e "${GREEN}✅ SETUP COMPLETE!${NC}"
echo ""
echo "To start X Assistant:"
echo "  systemctl start x-assistant"
echo ""
echo "To check status:"
echo "  systemctl status x-assistant"
echo ""
echo "To view logs:"
echo "  journalctl -u x-assistant -f"
echo ""
echo -e "${YELLOW}Then connect Cloudflare tunnel:${NC}"
echo "  cloudflared tunnel --url http://localhost:8000"
echo ""
echo "🎉 You're all set!"
