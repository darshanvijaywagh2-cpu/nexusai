#!/usr/bin/env python3
"""
X AI Avatar - Advanced Version
Eye blinking, movements, all expressions, multi-language!

pip install pyttsx3 gtts opencv-python numpy pygame

Run: python3 avatar_advanced.py
"""

import cv2
import numpy as np
import threading
import time
import queue
import os
import random

class XAvatarAdvanced:
    def __init__(self):
        self.mood = "neutral"
        self.speaking = False
        self.listening = False
        self.thinking = False
        self.blink_timer = 0
        self.blink_state = False
        self.eye_direction = (0, 0)  # (x, y) movement
        self.head_tilt = 0
        self.frame_count = 0
        
        # Config
        self.width = 500
        self.height = 600
        
        # Colors
        self.skin = (235, 200, 170)
        self.skin_dark = (200, 160, 130)
        self.eyes_white = (255, 255, 255)
        self.iris = (80, 100, 180)
        self.pupil = (20, 20, 20)
        self.mouth_color = (120, 60, 60)
        self.hair = (40, 30, 20)
        
        # Multi-language
        self.lang = "en"
        
        # Expression states
        self.expressions = {
            "neutral": {"eyebrow_raise": 0, "mouth_curve": 0, "cheek_raise": 0},
            "happy": {"eyebrow_raise": 10, "mouth_curve": 30, "cheek_raise": 15},
            "sad": {"eyebrow_raise": -10, "mouth_curve": -20, "cheek_raise": -10},
            "excited": {"eyebrow_raise": 20, "mouth_curve": 40, "cheek_raise": 20},
            "angry": {"eyebrow_raise": -15, "mouth_curve": -15, "cheek_raise": -5},
            "surprised": {"eyebrow_raise": 30, "mouth_curve": 10, "cheek_raise": 10},
            "thinking": {"eyebrow_raise": 5, "mouth_curve": -5, "cheek_raise": 0},
            "sleeping": {"eyebrow_raise": 0, "mouth_curve": 0, "cheek_raise": 0}
        }
        
    def draw_head(self, canvas):
        """Draw head shape"""
        center_x = self.width // 2
        center_y = self.height // 2 - 30
        
        # Face oval
        cv2.ellipse(canvas, (center_x, center_y), (160, 200), 0, 0, 360, self.skin, -1)
        
        # Neck
        cv2.rectangle(canvas, (center_x - 50, center_y + 170), 
                     (center_x + 50, center_y + 250), self.skin_dark, -1)
        
        # Hair
        cv2.ellipse(canvas, (center_x, center_y - 80), (170, 120), 0, 180, 360, self.hair, -1)
        
        # Side hair
        cv2.ellipse(canvas, (center_x - 150, center_y), (40, 150), 0, 0, 180, self.hair, -1)
        cv2.ellipse(canvas, (center_x + 150, center_y), (40, 150), 0, 0, 180, self.hair, -1)
        
        return canvas
    
    def draw_eyes(self, canvas):
        """Draw eyes with blinking and movement"""
        center_x = self.width // 2
        center_y = self.height // 2 - 50
        
        # Eye positions
        left_eye_x = center_x - 55
        right_eye_x = center_x + 55
        eye_y = center_y
        
        # Blink logic
        self.frame_count += 1
        if self.blink_timer > 0:
            self.blink_timer -= 1
            self.blink_state = True
        else:
            # Random blink every 2-5 seconds
            if random.random() < 0.005:
                self.blink_timer = 5
                self.blink_state = True
            else:
                self.blink_state = False
        
        # Eye direction (looking around)
        if self.listening:
            # Look around slowly
            self.eye_direction = (int(20 * np.sin(self.frame_count * 0.05)), 
                                  int(10 * np.cos(self.frame_count * 0.03)))
        elif self.thinking:
            # Look up and to side
            self.eye_direction = (20, -15)
        else:
            # Random small movements
            if random.random() < 0.02:
                self.eye_direction = (random.randint(-20, 20), random.randint(-15, 15))
        
        eye_offset_x, eye_offset_y = self.eye_direction
        
        for eye_x in [left_eye_x, right_eye_x]:
            if self.blink_state:
                # Closed eye (line)
                cv2.line(canvas, (eye_x - 25, eye_y), (eye_x + 25, eye_y), self.hair, 4)
            else:
                # White
                cv2.ellipse(canvas, (eye_x, eye_y), (30, 22), 0, 0, 360, self.eyes_white, -1)
                cv2.ellipse(canvas, (eye_x, eye_y), (30, 22), 0, 0, 360, (50, 50, 50), 2)
                
                # Iris
                iris_x = eye_x + int(eye_offset_x * 0.5)
                iris_y = eye_y + int(eye_offset_y * 0.5)
                cv2.circle(canvas, (iris_x, iris_y), 14, self.iris, -1)
                
                # Pupil
                cv2.circle(canvas, (iris_x + int(eye_offset_x * 0.3), 
                                   iris_y + int(eye_offset_y * 0.3)), 7, self.pupil, -1)
                
                # Eye highlight
                cv2.circle(canvas, (iris_x - 4, iris_y - 4), 4, (255, 255, 255), -1)
        
        return canvas
    
    def draw_eyebrows(self, canvas):
        """Draw eyebrows with expressions"""
        center_x = self.width // 2
        center_y = self.height // 2 - 90
        
        expr = self.expressions.get(self.mood, self.expressions["neutral"])
        brow_raise = expr["eyebrow_raise"]
        
        # Left eyebrow
        left_start = (center_x - 90, center_y + brow_raise)
        left_end = (center_x - 20, center_y - 10 + brow_raise)
        cv2.line(canvas, left_start, left_end, self.hair, 5)
        
        # Right eyebrow
        right_start = (center_x + 20, center_y - 10 + brow_raise)
        right_end = (center_x + 90, center_y + brow_raise)
        cv2.line(canvas, right_start, right_end, self.hair, 5)
        
        return canvas
    
    def draw_mouth(self, canvas):
        """Draw mouth with expressions"""
        center_x = self.width // 2
        mouth_y = self.height // 2 + 70
        
        expr = self.expressions.get(self.mood, self.expressions["neutral"])
        mouth_curve = expr["mouth_curve"]
        
        if self.speaking:
            # Animated mouth when speaking
            open_amount = int(15 + 10 * np.sin(self.frame_count * 0.3))
            cv2.ellipse(canvas, (center_x, mouth_y), (30, open_amount), 0, 0, 360, 
                       self.mouth_color, -1)
            # Teeth
            cv2.rectangle(canvas, (center_x - 20, mouth_y - open_amount + 5),
                         (center_x + 20, mouth_y), (255, 255, 255), -1)
        elif self.mood == "happy" or self.mood == "excited":
            # Big smile
            cv2.ellipse(canvas, (center_x, mouth_y + 10), (50, 25 + mouth_curve//2), 0, 0, 180, 
                       self.mouth_color, -1)
            # Teeth
            cv2.ellipse(canvas, (center_x, mouth_y + 10), (35, 15), 0, 0, 180, 
                       (255, 255, 255), -1)
        elif self.mood == "sad":
            # Frown
            cv2.ellipse(canvas, (center_x, mouth_y + 20), (35, 15), 0, 180, 360, 
                       self.mouth_color, 3)
        elif self.mood == "angry":
            # Tight lips
            cv2.line(canvas, (center_x - 25, mouth_y), (center_x + 25, mouth_y), 
                    self.mouth_color, 4)
        elif self.mood == "surprised":
            # O mouth
            cv2.circle(canvas, (center_x, mouth_y), 20, self.mouth_color, -1)
        else:
            # Neutral
            cv2.ellipse(canvas, (center_x, mouth_y), (30, 10), 0, 0, 180, 
                       self.mouth_color, 3)
        
        return canvas
    
    def draw_nose(self, canvas):
        """Draw nose"""
        center_x = self.width // 2
        nose_y = self.height // 2 + 10
        
        # Nose shape
        cv2.ellipse(canvas, (center_x, nose_y), (15, 20), 0, 0, 360, self.skin_dark, 2)
        
        return canvas
    
    def draw_cheeks(self, canvas):
        """Draw rosy cheeks"""
        center_x = self.width // 2
        cheek_y = self.height // 2 + 30
        
        expr = self.expressions.get(self.mood, self.expressions["neutral"])
        cheek_raise = expr["cheek_raise"]
        
        if cheek_raise > 0:
            # Rosy cheeks
            cv2.circle(canvas, (center_x - 100, cheek_y), 25 + cheek_raise, 
                      (180, 150, 150), -1)
            cv2.circle(canvas, (center_x + 100, cheek_y), 25 + cheek_raise, 
                      (180, 150, 150), -1)
        
        return canvas
    
    def set_mood(self, mood):
        """Set mood"""
        if mood in self.expressions:
            self.mood = mood
            print(f"Mood: {mood}")
    
    def set_language(self, lang):
        """Set language"""
        self.lang = lang
        print(f"Language: {lang}")
    
    def render(self):
        """Render the avatar"""
        # Create canvas
        canvas = np.ones((self.height, self.width, 3), dtype=np.uint8) * 50
        
        # Background gradient
        for i in range(self.height):
            cv2.line(canvas, (0, i), (self.width, i), 
                    (50 + i // 5, 50 + i // 5, 70 + i // 5), 1)
        
        # Draw face components
        canvas = self.draw_head(canvas)
        canvas = self.draw_cheeks(canvas)
        canvas = self.draw_eyes(canvas)
        canvas = self.draw_eyebrows(canvas)
        canvas = self.draw_nose(canvas)
        canvas = self.draw_mouth(canvas)
        
        # Status indicator
        if self.listening:
            cv2.putText(canvas, "🎤 Listening...", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 255, 100), 2)
        elif self.speaking:
            cv2.putText(canvas, "🔊 Speaking...", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 200, 100), 2)
        elif self.thinking:
            cv2.putText(canvas, "🤔 Thinking...", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 255), 2)
        
        # Mood label
        cv2.putText(canvas, f"Mood: {self.mood.upper()}", (10, self.height - 20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
        
        return canvas
    
    def run(self):
        """Main loop"""
        print("""
╔═══════════════════════════════════════════╗
║       🤖 X AVATAR - ADVANCED            ║
╠═══════════════════════════════════════════╣
║  Commands:                               ║
║  n - neutral    h - happy               ║
║  s - sad        e - excited             ║
║  a - angry      u - surprised           ║
║  t - thinking   z - sleeping            ║
║  l - listen     q - quit                ║
║                                           ║
║  Languages: en hi es fr de ja zh         ║
╚═══════════════════════════════════════════╝
        """)
        
        while True:
            frame = self.render()
            cv2.imshow("X - AI Avatar", frame)
            
            key = cv2.waitKey(50) & 0xFF
            
            if key == ord('q'):
                break
            elif key == ord('n'):
                self.set_mood("neutral")
            elif key == ord('h'):
                self.set_mood("happy")
            elif key == ord('s'):
                self.set_mood("sad")
            elif key == ord('e'):
                self.set_mood("excited")
            elif key == ord('a'):
                self.set_mood("angry")
            elif key == ord('u'):
                self.set_mood("surprised")
            elif key == ord('t'):
                self.set_mood("thinking")
                self.thinking = True
            elif key == ord('z'):
                self.set_mood("sleeping")
            elif key == ord('l'):
                self.listening = not self.listening
                self.thinking = False
            elif key == ord('1'):
                self.set_language("en")
            elif key == ord('2'):
                self.set_language("hi")
        
        cv2.destroyAllWindows()

if __name__ == "__main__":
    avatar = XAvatarAdvanced()
    avatar.run()
