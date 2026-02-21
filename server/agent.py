#!/usr/bin/env python3
"""
X AI - Enhanced Desktop Bridge Agent
With logging, heartbeat, and auto-reconnect
"""

import requests
import json
import time
import os
import logging
from datetime import datetime

# Setup logging
log_file = "/tmp/nexusai_agent.log"
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger().addHandler(console)

class DesktopAgent:
    def __init__(self):
        # Configuration
        self.vps_url = os.environ.get('VPS_URL', 'https://superintendent-info-smooth-gordon.trycloudflare.com')
        self.desktop_id = os.environ.get('DESKTOP_ID', 'desktop-1')
        self.check_interval = 5  # seconds
        self.running = True
        self.registered = False
        
        logging.info(f"Agent initializing...")
        logging.info(f"VPS URL: {self.vps_url}")
        logging.info(f"Desktop ID: {self.desktop_id}")
        
    def register(self):
        """Register with VPS"""
        try:
            response = requests.post(
                f"{self.vps_url}/bridge/register",
                json={
                    "desktop_id": self.desktop_id,
                    "status": "online",
                    "registered_at": datetime.now().isoformat()
                },
                timeout=10
            )
            if response.status_code == 200:
                self.registered = True
                logging.info(f"✅ Registered with VPS as {self.desktop_id}")
                return True
            else:
                logging.warning(f"Registration failed: {response.status_code}")
        except Exception as e:
            logging.error(f"❌ Registration error: {e}")
        return False
    
    def heartbeat(self):
        """Send heartbeat to VPS"""
        try:
            response = requests.post(
                f"{self.vps_url}/bridge/heartbeat",
                json={
                    "desktop_id": self.desktop_id,
                    "status": "online",
                    "timestamp": datetime.now().isoformat()
                },
                timeout=5
            )
            if response.status_code == 200:
                logging.debug(f"💓 Heartbeat sent")
                return True
        except Exception as e:
            logging.warning(f"⚠️ Heartbeat failed: {e}")
        return False
    
    def get_commands(self):
        """Get pending commands from VPS"""
        try:
            response = requests.get(
                f"{self.vps_url}/bridge/commands?desktop_id={self.desktop_id}",
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                return data.get("commands", [])
        except Exception as e:
            logging.debug(f"Commands fetch: {e}")
        return []
    
    def execute_command(self, command: dict):
        """Execute command locally"""
        cmd = command.get("command", "")
        params = command.get("params", {})
        
        logging.info(f"📥 Executing: {cmd}")
        
        result = {"status": "success", "output": ""}
        
        try:
            if cmd == "open_browser" or cmd == "browser_open":
                import subprocess
                url = params.get("url", "https://google.com")
                subprocess.run(["xdg-open", url], check=True)
                result["output"] = f"Opened: {url}"
                logging.info(f"✅ {result['output']}")
                
            elif cmd == "type":
                import subprocess
                text = params.get("text", "")
                escaped = text.replace("'", "'\\''")
                subprocess.run(f"xdotool type -- '{escaped}'", shell=True, check=True)
                result["output"] = f"Typed: {text[:50]}"
                logging.info(f"✅ {result['output']}")
                
            elif cmd == "click":
                import subprocess
                x = params.get("x", 0)
                y = params.get("y", 0)
                subprocess.run(["xdotool", "mousemove", str(x), str(y), "click", "1"], check=True)
                result["output"] = f"Clicked: {x},{y}"
                logging.info(f"✅ {result['output']}")
                
            elif cmd == "screenshot":
                import subprocess
                subprocess.run(["gnome-screenshot", "-f", "/tmp/desktop_cap.png"], check=True)
                result["output"] = "/tmp/desktop_cap.png"
                logging.info(f"✅ Screenshot saved")
                
            elif cmd == "spotify_play":
                import subprocess
                subprocess.run(["playerctl", "-p", "spotify", "play"], check=True)
                result["output"] = "Spotify playing"
                logging.info(f"✅ Spotify play")
                
            elif cmd == "spotify_next":
                import subprocess
                subprocess.run(["playerctl", "-p", "spotify", "next"], check=True)
                result["output"] = "Next track"
                logging.info(f"✅ Spotify next")
                
            elif cmd == "volume":
                import subprocess
                level = params.get("level", 50)
                subprocess.run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", f"{level}%"], check=True)
                result["output"] = f"Volume: {level}%"
                logging.info(f"✅ {result['output']}")
                
            else:
                result["output"] = f"Unknown command: {cmd}"
                logging.warning(f"❌ {result['output']}")
                
        except Exception as e:
            result["status"] = "error"
            result["output"] = str(e)
            logging.error(f"❌ Error: {e}")
        
        return result
    
    def report_result(self, command_id: str, result: dict):
        """Report command result to VPS"""
        try:
            requests.post(
                f"{self.vps_url}/bridge/result",
                json={
                    "command_id": command_id,
                    "desktop_id": self.desktop_id,
                    "result": result,
                    "timestamp": datetime.now().isoformat()
                },
                timeout=10
            )
            logging.info(f"📤 Result reported for {command_id}")
        except Exception as e:
            logging.debug(f"Result report: {e}")
    
    def run(self):
        """Main loop"""
        logging.info("""
╔═══════════════════════════════════╗
║     X DESKTOP AGENT v2.0        ║
╠═══════════════════════════════════╣
║  Hybrid Production Ready!        ║
╚═══════════════════════════════════╝
        """)
        
        # Register with VPS
        if not self.register():
            logging.warning("⚠️ Running without VPS connection")
        
        # Main loop
        while self.running:
            try:
                # Send heartbeat
                self.heartbeat()
                
                # Get and execute commands
                commands = self.get_commands()
                for cmd in commands:
                    result = self.execute_command(cmd)
                    self.report_result(cmd.get("id"), result)
                
                time.sleep(self.check_interval)
                
            except KeyboardInterrupt:
                logging.info("👋 Shutting down...")
                self.running = False
            except Exception as e:
                logging.error(f"❌ Loop error: {e}")
                time.sleep(5)

if __name__ == "__main__":
    agent = DesktopAgent()
    agent.run()
