#!/usr/bin/env python3
"""
X AI Avatar - Animated Desktop Character
Real-time lip sync and expressions!

Requirements:
pip install pyttsx3 gtts opencv-python pillow numpy

Run: python3 avatar.py
"""

import cv2
import numpy as np
import pyttsx3
import threading
import time
import queue
import os

# Avatar configuration
class XAvatar:
    def __init__(self):
        self.mood = "happy"
        self.speaking = False
        self.listening = False
        self.width = 400
        self.height = 400
        
        # Colors
        self.colors = {
            "skin": (255, 220, 177),
            "eyes": (50, 50, 50),
            "mouth": (150, 50, 50),
            "happy": (255, 200, 100),
            "sad": (100, 150, 200),
            "excited": (255, 100, 100)
        }
        
        # TTS Engine
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 1.0)
        
        # Audio queue for lip sync
        self.audio_queue = queue.Queue()
        
    def draw_face(self):
        """Draw the avatar face"""
        # Create canvas
        canvas = np.ones((self.height, self.width, 3), dtype=np.uint8) * 240
        
        # Face circle
        center = (self.width // 2, self.height // 2)
        radius = 150
        cv2.circle(canvas, center, radius, self.colors["skin"], -1)
        
        # Eyes
        eye_y = center[1] - 40
        left_eye = (center[0] - 50, eye_y)
        right_eye = (center[0] + 50, eye_y)
        
        if self.listening:
            # Big listening eyes
            cv2.circle(canvas, left_eye, 25, (255, 255, 255), -1)
            cv2.circle(canvas, right_eye, 25, (255, 255, 255), -1)
            cv2.circle(canvas, left_eye, 15, self.colors["eyes"], -1)
            cv2.circle(canvas, right_eye, 15, self.colors["eyes"], -1)
        else:
            # Normal eyes
            cv2.circle(canvas, left_eye, 20, (255, 255, 255), -1)
            cv2.circle(canvas, right_eye, 20, (255, 255, 255), -1)
            cv2.circle(canvas, left_eye, 12, self.colors["eyes"], -1)
            cv2.circle(canvas, right_eye, 12, self.colors["eyes"], -1)
        
        # Eyebrows
        brow_y = eye_y - 35
        cv2.line(canvas, (left_eye[0] - 25, brow_y), (left_eye[0] + 25, brow_y), self.colors["eyes"], 3)
        cv2.line(canvas, (right_eye[0] - 25, brow_y), (right_eye[0] + 25, brow_y), self.colors["eyes"], 3)
        
        # Mouth
        mouth_y = center[1] + 50
        if self.speaking:
            # Open mouth when speaking
            mouth_width = 60
            mouth_height = 30
            cv2.ellipse(canvas, (center[0], mouth_y), (mouth_width, mouth_height), 0, 0, 180, self.colors["mouth"], -1)
        elif self.mood == "happy":
            # Smile
            cv2.arcStart = (center[0] - 50, mouth_y - 20)
            cv2.arcEnd = (center[0] + 50, mouth_y + 20)
            cv2.ellipse(canvas, (center[0], mouth_y), (50, 30), 0, 0, 180, self.colors["mouth"], 3)
        elif self.mood == "sad":
            # Frown
            cv2.ellipse(canvas, (center[0], mouth_y + 20), (40, 20), 0, 180, 360, self.colors["mouth"], 3)
        elif self.mood == "excited":
            # Big smile
            cv2.ellipse(canvas, (center[0], mouth_y), (60, 40), 0, 0, 180, self.colors["mouth"], 3)
        else:
            # Neutral
            cv2.line(canvas, (center[0] - 30, mouth_y), (center[0] + 30, mouth_y), self.colors["mouth"], 3)
        
        # Add mood color indicator
        mood_color = self.colors.get(self.mood, self.colors["happy"])
        cv2.circle(canvas, (self.width - 40, 40), 20, mood_color, -1)
        
        return canvas
    
    def set_mood(self, mood):
        """Change mood"""
        self.mood = mood
        print(f"Mood: {mood}")
    
    def speak(self, text):
        """Speak and animate"""
        self.speaking = True
        
        # Speak in thread
        def speak_thread():
            self.engine.say(text)
            self.engine.runAndWait()
            self.speaking = False
        
        thread = threading.Thread(target=speak_thread)
        thread.start()
        
        # Animate while speaking
        while self.speaking:
            frame = self.draw_face()
            cv2.imshow("X - AI Avatar", frame)
            if cv2.waitKey(50) & 0xFF == ord('q'):
                break
        
        thread.join()
        self.speaking = False
    
    def listen_mode(self, active=True):
        """Listening animation"""
        self.listening = active
        if active:
            print("👂 Listening...")
            while self.listening:
                frame = self.draw_face()
                cv2.imshow("X - AI Avatar", frame)
                if cv2.waitKey(100) & 0xFF == ord('q'):
                    break
        self.listening = False
    
    def run(self):
        """Main loop"""
        print("""
╔═══════════════════════════════════╗
║       🤖 X - AI AVATAR           ║
╠═══════════════════════════════════╣
║  Commands:                        ║
║  - happy / sad / excited          ║
║  - say [message]                  ║
║  - listen                         ║
║  - quit                           ║
╚═══════════════════════════════════╝
        """)
        
        while True:
            frame = self.draw_face()
            cv2.imshow("X - AI Avatar", frame)
            
            key = cv2.waitKey(100) & 0xFF
            
            if key == ord('q'):
                break
            elif key == ord('h'):
                self.set_mood("happy")
            elif key == ord('s'):
                self.set_mood("sad")
            elif key == ord('e'):
                self.set_mood("excited")
        
        cv2.destroyAllWindows()

if __name__ == "__main__":
    avatar = XAvatar()
    avatar.run()
