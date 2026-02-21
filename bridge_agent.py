#!/usr/bin/env python3
"""
X AI - Hybrid Bridge Agent
Runs on Desktop, connects to VPS for commands
"""

import requests
import json
import time
import os

# Configuration
VPS_URL = os.environ.get('VPS_URL', 'http://localhost:8000')
DESKTOP_ID = os.environ.get('DESKTOP_ID', 'desktop-1')
CHECK_INTERVAL = 5  # seconds

class HybridBridge:
    def __init__(self):
        self.vps_url = VPS_URL
        self.desktop_id = DESKTOP_ID
        self.registered = False
        
    def register(self):
        """Register with VPS"""
        try:
            response = requests.post(
                f"{self.vps_url}/bridge/register",
                json={"desktop_id": self.desktop_id, "status": "online"},
                timeout=10
            )
            if response.status_code == 200:
                self.registered = True
                print(f"✅ Registered with VPS as {self.desktop_id}")
                return True
        except Exception as e:
            print(f"❌ Registration failed: {e}")
        return False
    
    def send_heartbeat(self):
        """Send heartbeat to VPS"""
        try:
            requests.post(
                f"{self.vps_url}/bridge/heartbeat",
                json={"desktop_id": self.desktop_id, "status": "online"},
                timeout=5
            )
        except:
            pass
    
    def get_commands(self):
        """Get pending commands from VPS"""
        try:
            response = requests.get(
                f"{self.vps_url}/bridge/commands?desktop_id={self.desktop_id}",
                timeout=10
            )
            if response.status_code == 200:
                return response.json().get("commands", [])
        except:
            pass
        return []
    
    def execute_command(self, command):
        """Execute command locally"""
        cmd = command.get("command", "")
        params = command.get("params", {})
        
        results = {"status": "success", "output": ""}
        
        try:
            if cmd == "open_browser":
                import subprocess
                subprocess.run(["xdg-open", params.get("url", "https://google.com")])
                results["output"] = "Browser opened"
                
            elif cmd == "type":
                import subprocess
                text = params.get("text", "")
                escaped = text.replace("'", "'\\''")
                subprocess.run(f"xdotool type -- '{escaped}'", shell=True)
                results["output"] = f"Typed: {text}"
                
            elif cmd == "click":
                import subprocess
                x = params.get("x", 0)
                y = params.get("y", 0)
                subprocess.run(["xdotool", "mousemove", str(x), str(y), "click", "1"])
                results["output"] = f"Clicked: {x},{y}"
                
            elif cmd == "screenshot":
                import subprocess
                subprocess.run(["gnome-screenshot", "-f", "/tmp/desktop_cap.png"])
                results["output"] = "/tmp/desktop_cap.png"
                
            elif cmd == "spotify_play":
                import subprocess
                subprocess.run(["playerctl", "-p", "spotify", "play"])
                results["output"] = "Spotify playing"
                
            elif cmd == "spotify_next":
                import subprocess
                subprocess.run(["playerctl", "-p", "spotify", "next"])
                results["output"] = "Next track"
                
            else:
                results["output"] = f"Unknown command: {cmd}"
                
        except Exception as e:
            results["status"] = "error"
            results["output"] = str(e)
        
        return results
    
    def report_result(self, command_id, results):
        """Report command result to VPS"""
        try:
            requests.post(
                f"{self.vps_url}/bridge/result",
                json={
                    "command_id": command_id,
                    "desktop_id": self.desktop_id,
                    "results": results
                },
                timeout=10
            )
        except:
            pass
    
    def run(self):
        """Main loop"""
        print("""
╔═══════════════════════════════════╗
║     X HYBRID BRIDGE AGENT       ║
╠═══════════════════════════════════╣
║  Connecting to VPS...           ║
║  Desktop automation ready!      ║
╚═══════════════════════════════════╝
        """)
        
        # Register with VPS
        if not self.register():
            print("⚠️ Running in standalone mode")
        
        print("🚀 Bridge started!")
        
        while True:
            # Get commands
            commands = self.get_commands()
            
            for cmd in commands:
                print(f"📥 Executing: {cmd.get('command')}")
                result = self.execute_command(cmd)
                self.report_result(cmd.get("id"), result)
            
            # Send heartbeat
            self.send_heartbeat()
            
            time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    bridge = HybridBridge()
    bridge.run()
