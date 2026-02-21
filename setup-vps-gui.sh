#!/bin/bash
# X AI - VPS GUI Desktop Setup
# Turn your VPS into a virtual desktop!

echo "🤖 Setting up X Desktop on VPS..."
echo "=================================="

# Install Xvfb (virtual display)
echo "📺 Installing virtual display..."
sudo apt update
sudo apt install -y xvfb x11vnc x11-utils

# Install GUI browsers
echo "🌐 Installing browsers..."
sudo apt install -y firefox chromium-browser chromium

# Install automation tools
echo "🔧 Installing automation tools..."
sudo apt install -y \
    python3-selenium \
    python3-playwright \
    chromium-driver

# Install desktop environment
echo "🖥️ Installing XFCE desktop..."
sudo apt install -y xfce4 xfce4-goodies

# Install media tools
echo "🎬 Installing media tools..."
sudo apt install -y \
    playerctl \
    ffmpeg \
    imagemagick

# Install Python automation
echo "🐍 Installing Python automation..."
pip3 install --break-system-packages \
    selenium \
    playwright \
    pyautogui \
    pytesseract

# Create X startup script
echo "📝 Creating startup scripts..."

# Xvfb startup
cat > ~/startxvfb << 'EOF'
#!/bin/bash
Xvfb :0 -screen 0 1920x1080x24 &
export DISPLAY=:0
echo "Xvfb started on :0"
EOF
chmod +x ~/startxvfb

# Browser automation script
cat > ~/browser_control.py << 'EOF'
#!/usr/bin/env python3
"""Browser automation for X Assistant"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import os

DISPLAY = os.environ.get('DISPLAY', ':0')

def get_browser():
    """Get Chrome browser with options"""
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument(f'--display={DISPLAY}')
    options.add_argument('--start-maximized')
    
    driver = webdriver.Chrome(options=options)
    return driver

def open_url(url):
    """Open URL in browser"""
    driver = get_browser()
    driver.get(url)
    return {"status": "success", "url": url, "title": driver.title}

def click_element(xpath):
    """Click element"""
    driver = get_browser()
    element = driver.find_element("xpath", xpath)
    element.click()
    return {"status": "success", "clicked": xpath}

def type_text(xpath, text):
    """Type text"""
    driver = get_browser()
    element = driver.find_element("xpath", xpath)
    element.send_keys(text)
    return {"status": "success", "typed": text}

def scroll_down(pixels=500):
    """Scroll page"""
    driver = get_browser()
    driver.execute_script(f"window.scrollBy(0,{pixels})")
    return {"status": "success", "scrolled": pixels}

def take_screenshot():
    """Take screenshot"""
    driver = get_browser()
    driver.save_screenshot("/tmp/x_screenshot.png")
    return {"status": "success", "file": "/tmp/x_screenshot.png"}

if __name__ == "__main__":
    print("Browser control ready!")
EOF

chmod +x ~/browser_control.py

# Create API for browser control
cat > ~/nexusai/server/browser_control.py << 'EOF'
"""Browser control endpoints for X AI"""
from fastapi import APIRouter
import subprocess
import os

router = APIRouter()
DISPLAY = os.environ.get('DISPLAY', ':0')

@router.get("/browser/open")
async def open_browser(url: str):
    """Open URL in browser"""
    try:
        subprocess.run(["firefox", url], 
                     env={**os.environ, 'DISPLAY': DISPLAY},
                     capture_output=True)
        return {"status": "success", "url": url}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.get("/browser/screenshot")
async def take_screenshot():
    """Take screenshot"""
    try:
        subprocess.run(["import", "-window", "root", "/tmp/vps_screenshot.png"],
                     env={**os.environ, 'DISPLAY': DISPLAY},
                     capture_output=True)
        return {"status": "success", "file": "/tmp/vps_screenshot.png"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.post("/browser/type")
async def type_text(text: str):
    """Type text"""
    try:
        subprocess.run(["xdotool", "type", text],
                     env={**os.environ, 'DISPLAY': DISPLAY},
                     capture_output=True)
        return {"status": "success", "typed": text}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.get("/browser/click")
async def mouse_click(x: int = 0, y: int = 0):
    """Click at position"""
    try:
        subprocess.run(["xdotool", "mousemove", str(x), str(y), "click", "1"],
                     env={**os.environ, 'DISPLAY': DISPLAY},
                     capture_output=True)
        return {"status": "success", "clicked": f"{x},{y}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
EOF

echo ""
echo "✅ SETUP COMPLETE!"
echo ""
echo "📝 TO START:"
echo "1. Start virtual display:"
echo "   ~/startxvfb"
echo ""
echo "2. Start X desktop:"
echo "   startx"
echo ""
echo "3. Access via VNC:"
echo "   x11vnc -display :0"
echo ""
echo "🔗 Then connect tunnel and control from Telegram!"
echo ""
echo "🎉 VPS Desktop ready!"
