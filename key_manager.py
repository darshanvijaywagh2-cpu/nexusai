#!/usr/bin/env python3
"""
X AI - Secure API Key Manager
Encrypts and stores API keys safely
"""

import os
import json
import base64
import hashlib
from cryptography.fernet import Fernet
from pathlib import Path

# Configuration
KEY_FILE = os.path.expanduser("~/.nexusai/keys.enc")
MASTER_PASSWORD = None

def generate_key(password: str) -> bytes:
    """Generate encryption key from password"""
    return base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest())

def initialize(password: str):
    """Initialize encrypted storage"""
    global MASTER_PASSWORD, f
    MASTER_PASSWORD = password
    f = Fernet(generate_key(password))
    
    # Create directory
    Path(os.path.dirname(KEY_FILE)).mkdir(parents=True, exist_ok=True)
    
    # Create new file if doesn't exist
    if not os.path.exists(KEY_FILE):
        save_keys({})

def load_keys() -> dict:
    """Load encrypted keys"""
    if not os.path.exists(KEY_FILE):
        return {}
    
    try:
        with open(KEY_FILE, 'rb') as file:
            encrypted = file.read()
            if encrypted:
                decrypted = f.decrypt(encrypted)
                return json.loads(decrypted)
    except:
        pass
    
    return {}

def save_keys(keys: dict):
    """Save encrypted keys"""
    with open(KEY_FILE, 'wb') as file:
        encrypted = f.encrypt(json.dumps(keys).encode())
        file.write(encrypted)

def set_key(name: str, value: str):
    """Set an API key"""
    keys = load_keys()
    keys[name] = value
    save_keys(keys)
    print(f"✅ Key '{name}' saved securely!")

def get_key(name: str) -> str:
    """Get an API key"""
    keys = load_keys()
    return keys.get(name, os.environ.get(name, ''))

def list_keys() -> list:
    """List stored key names (not values)"""
    keys = load_keys()
    return list(keys.keys())

def delete_key(name: str):
    """Delete a key"""
    keys = load_keys()
    if name in keys:
        del keys[name]
        save_keys(keys)
        print(f"✅ Key '{name}' deleted!")

def setup():
    """Interactive setup"""
    print("""
╔═══════════════════════════════════╗
║   X API KEY MANAGER           ║
╠═══════════════════════════════════╣
║  Secure encrypted storage     ║
╚═══════════════════════════════════╝
    """)
    
    password = input("Create master password: ")
    initialize(password)
    
    print("\nAdd API keys:")
    print("1. OpenAI")
    print("2. Anthropic (Claude)")
    print("3. Gemini")
    print("4. Groq")
    print("5. Custom")
    print("6. Exit")
    
    while True:
        choice = input("\nChoice: ")
        
        if choice == "1":
            key = input("OpenAI API Key: ")
            set_key("OPENAI_API_KEY", key)
        elif choice == "2":
            key = input("Anthropic API Key: ")
            set_key("ANTHROPIC_API_KEY", key)
        elif choice == "3":
            key = input("Gemini API Key: ")
            set_key("GEMINI_API_KEY", key)
        elif choice == "4":
            key = input("Groq API Key: ")
            set_key("GROQ_API_KEY", key)
        elif choice == "5":
            name = input("Key name: ")
            key = input(f"{name}: ")
            set_key(name.upper(), key)
        elif choice == "6":
            break
    
    print(f"\n✅ Keys saved to: {KEY_FILE}")
    print("🔐 Encrypted with your master password!")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == "setup":
            setup()
        elif sys.argv[1] == "list":
            print("Stored keys:", list_keys())
        elif sys.argv[1] == "get" and len(sys.argv) > 2:
            print(get_key(sys.argv[2]))
        elif sys.argv[1] == "set" and len(sys.argv) > 3:
            initialize(sys.argv[2])
            set_key(sys.argv[3], sys.argv[4])
    else:
        print("Usage:")
        print("  python3 key_manager.py setup")
        print("  python3 key_manager.py list")
        print("  python3 key_manager.py get KEY_NAME")
        print("  python3 key_manager.py set PASSWORD KEY_NAME VALUE")
