#!/bin/bash
# X AI Desktop Auto-Setup
# Auto-start on boot + connect to VPS

echo "🤖 Setting up X Desktop Agent..."
echo "================================"

# Update
echo "📦 Updating..."
sudo apt update && sudo apt upgrade -y

# Install dependencies
echo "🛠️ Installing tools..."
sudo apt install -y xdotool wmctrl gnome-screenshot playerctl git python3-pip curl

# Download code
echo "📥 Downloading..."
cd ~
git clone https://github.com/darshanvijaywagh2-cpu/nexusai.git

# Install Python packages
echo "🐍 Installing Python..."
pip3 install --break-system-packages requests fastapi uvicorn pillow

# Create service
echo "📝 Creating service..."
sudo cp ~/nexusai/nexusai-agent.service /etc/systemd/system/

# Edit VPS URL
echo "Enter your VPS URL (or press Enter for local):"
read -r VPS_URL

if [ -n "$VPS_URL" ]; then
    sudo sed -i "s|Environment=VPS_URL=|Environment=VPS_URL=$VPS_URL|" /etc/systemd/system/nexusai-agent.service
fi

# Enable service
echo "🔄 Enabling service..."
sudo systemctl daemon-reload
sudo systemctl enable nexusai-agent
sudo systemctl start nexusai-agent

# Status
echo ""
echo "✅ SETUP COMPLETE!"
echo ""
echo "Check status:"
echo "  sudo systemctl status nexusai-agent"
echo ""
echo "View logs:"
echo "  journalctl -u nexusai-agent -f"
echo ""
echo "🎉 Agent will auto-start on boot!"
