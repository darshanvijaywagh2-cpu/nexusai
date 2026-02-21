#!/usr/bin/env python3
"""
X AI - Desktop Manager
Manages desktop connection status
"""

import time
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    filename='/tmp/desktop_manager.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class DesktopManager:
    def __init__(self):
        self.desktops = {}  # {desktop_id: last_seen}
        self.timeout = 15  # seconds
        
    def register_desktop(self, desktop_id: str):
        """Register a new desktop"""
        self.desktops[desktop_id] = time.time()
        logging.info(f"Desktop registered: {desktop_id}")
        
    def update_heartbeat(self, desktop_id: str):
        """Update desktop heartbeat"""
        self.desktops[desktop_id] = time.time()
        logging.debug(f"Heartbeat: {desktop_id}")
        
    def is_online(self, desktop_id: str) -> bool:
        """Check if desktop is online"""
        if desktop_id not in self.desktops:
            return False
        
        last_seen = self.desktops[desktop_id]
        return (time.time() - last_seen) < self.timeout
    
    def get_status(self, desktop_id: str = None):
        """Get desktop status"""
        if desktop_id:
            return {
                "desktop_id": desktop_id,
                "online": self.is_online(desktop_id),
                "last_seen": datetime.fromtimestamp(self.desktops.get(desktop_id, 0)).isoformat()
            }
        
        # All desktops
        return {
            desktop_id: {
                "online": self.is_online(desktop_id),
                "last_seen": datetime.fromtimestamp(last_seen).isoformat()
            }
            for desktop_id, last_seen in self.desktops.items()
        }
    
    def route_command(self, command: str, desktop_id: str = "desktop-1"):
        """Route command to desktop or headless"""
        if self.is_online(desktop_id):
            return {
                "route": "desktop",
                "desktop_id": desktop_id,
                "message": "Sending to online desktop"
            }
        else:
            return {
                "route": "headless",
                "desktop_id": desktop_id,
                "message": "Desktop offline - using VPS headless"
            }

# Global instance
manager = DesktopManager()
