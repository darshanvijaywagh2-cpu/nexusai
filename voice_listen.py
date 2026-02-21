#!/usr/bin/env python3
"""
X AI Assistant - Continuous Voice Listening
Run this on desktop for hands-free control!
"""

import speech_recognition as sr
import pvporcupine
import pyttsx3
import os
import sys

# Configuration
WAKE_WORD = "hey x"
LISTENING = True

# Text to speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)

def speak(text):
    """Speak the text"""
    print(f"X: {text}")
    engine.say(text)
    engine.runAndWait()

def listen_for_wake_word():
    """Listen for wake word using porcupine"""
    print("🎤 Listening for 'Hey X'...")
    
    # Initialize porcupine for wake word detection
    try:
        porcupine = pvporcupine.create(
            keywords=["hey x", "alexa"]
        )
        print("✓ Wake word engine ready!")
    except Exception as e:
        print(f"⚠️ Wake word error: {e}")
        print("Using fallback listening...")
        return listen_fallback()

    # Get microphone
    pa = sr.Microphone()
    rec = sr.Recognizer()

    with pa as source:
        rec.adjust_for_ambient_noise(source)

    print("👂 Listening...")

    try:
        with sr.Microphone() as source:
            while LISTENING:
                audio = rec.listen(source, timeout=5, phrase_time_limit=10)
                
                # Check for wake word using porcupine
                keyword_index = porcupine.process(audio.frame_data)
                
                if keyword_index >= 0:
                    print("🎯 Wake word detected!")
                    speak("Yes?")
                    listen_command(rec, source)
                    
    except Exception as e:
        print(f"Error: {e}")
        listen_for_wake_word()

def listen_fallback():
    """Fallback simple listening"""
    rec = sr.Recognizer()
    
    print("👂 Simple listening mode...")
    
    with sr.Microphone() as source:
        rec.adjust_for_ambient_noise(source)
        
        while LISTENING:
            try:
                audio = rec.listen(source, timeout=5, phrase_time_limit=10)
                text = rec.recognize_google(audio).lower()
                
                if WAKE_WORD in text:
                    print(f" Heard: {text}")
                    speak("Yes?")
                    listen_command(rec, source)
                    
            except:
                pass

def listen_command(rec, source):
    """Listen for command after wake word"""
    print("🎤 Waiting for command...")
    
    try:
        audio = rec.listen(source, timeout=10, phrase_time_limit=15)
        command = rec.recognize_google(audio).lower()
        
        print(f"📝 Command: {command}")
        process_command(command)
        
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
    except sr.RequestError:
        speak("Sorry, I'm having trouble connecting.")

def process_command(command):
    """Process the voice command"""
    # API call would go here
    responses = {
        "hello": "Hello! How can I help?",
        "time": f"It's {__import__('datetime').datetime.now().strftime('%I:%M %p')}",
        "date": f"Today is {__import__('datetime').datetime.now().strftime('%B %d, %Y')}",
        "weather": "Let me check the weather for you...",
    }
    
    for key, response in responses.items():
        if key in command:
            speak(response)
            return
    
    speak(f"You said: {command}")

def main():
    print("""
╔═══════════════════════════════╗
║    🤖 X - Voice Assistant    ║
╠═══════════════════════════════╣
║  Say "Hey X" to activate     ║
║  Say "stop" to exit          ║
╚═══════════════════════════════╝
    """)
    
    speak("X is now online. Say Hey X to activate.")
    
    try:
        listen_for_wake_word()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        LISTENING = False

if __name__ == "__main__":
    main()
