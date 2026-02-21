#!/usr/bin/env python3
"""
X AI - Headless Browser Automation
For VPS when desktop is offline
"""

import time
import random
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    filename='/tmp/headless.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class HeadlessBrowser:
    def __init__(self):
        self.browser = None
        self.context = None
        self.page = None
        
    def launch(self, headless: bool = True):
        """Launch headless browser"""
        try:
            from playwright.sync_api import sync_playwright
            
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch(headless=headless)
            self.context = self.browser.new_context(
                viewport={'width': 1920, '1080'}
            )
            self.page = self.context.new_page()
            logging.info("Headless browser launched")
            return True
        except Exception as e:
            logging.error(f"Browser launch failed: {e}")
            return False
            
    def random_delay(self, min_sec: int = 2, max_sec: int = 5):
        """Human-like random delay"""
        delay = random.randint(min_sec, max_sec)
        time.sleep(delay)
        
    def scroll_human(self):
        """Human-like scrolling"""
        for _ in range(random.randint(3, 8)):
            self.page.mouse.wheel(0, random.randint(300, 800))
            time.sleep(random.randint(1, 3))
            
    def open_instagram(self, username: str = None):
        """Open Instagram"""
        if not self.browser:
            self.launch()
            
        self.page.goto("https://www.instagram.com/")
        self.random_delay(3, 6)
        
        if username:
            self.page.goto(f"https://www.instagram.com/{username}/")
            self.random_delay(2, 4)
            
        logging.info("Instagram opened")
        return {"status": "success", "url": self.page.url}
    
    def open_whatsapp(self):
        """Open WhatsApp Web"""
        if not self.browser:
            self.launch()
            
        self.page.goto("https://web.whatsapp.com/")
        self.random_delay(5, 10)
        
        logging.info("WhatsApp opened")
        return {"status": "success", "url": self.page.url}
    
    def open_twitter(self):
        """Open Twitter/X"""
        if not self.browser:
            self.launch()
            
        self.page.goto("https://x.com/")
        self.random_delay(3, 5)
        
        logging.info("Twitter opened")
        return {"status": "success", "url": self.page.url}
    
    def search_google(self, query: str):
        """Search on Google"""
        if not self.browser:
            self.launch()
            
        self.page.goto(f"https://www.google.com/search?q={query}")
        self.random_delay(2, 4)
        
        logging.info(f"Google search: {query}")
        return {"status": "success", "query": query}
    
    def take_screenshot(self, path: str = "/tmp/headless_screenshot.png"):
        """Take screenshot"""
        if self.page:
            self.page.screenshot(path=path)
            logging.info(f"Screenshot: {path}")
            return {"status": "success", "file": path}
        return {"status": "error", "message": "No page"}
        
    def close(self):
        """Close browser"""
        if self.browser:
            self.browser.close()
            logging.info("Browser closed")

# Global instance
headless = HeadlessBrowser()
