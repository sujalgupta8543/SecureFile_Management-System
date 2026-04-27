from cryptography.fernet import Fernet
import os

KEY_FILE = "secret.key"

def load_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            return f.read()
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
        return key

key = load_key()
cipher = Fernet(key)

def encrypt_data(data):
    return cipher.encrypt(data.encode())

def decrypt_data(data):
    return cipher.decrypt(data).decode()

def validate_input(data, max_length=500):
    """Detects buffer overflow attempts by checking input length."""
    if len(data) > max_length:
        print(f"[ALERT] Buffer Overflow Attempt Detected: {len(data)} characters!")
        return False
    return True

def detect_malware(content):
    """Improved malware detection using common malicious signatures."""
    suspicious_patterns = [
        "virus", "trojan", "malware", "exploit", "shellcode", 
        "<script>", "eval(", "os.system", "subprocess", "base64.b64decode"
    ]
    content_lower = content.lower()
    for pattern in suspicious_patterns:
        if pattern in content_lower:
            print(f"[ALERT] Security Threat Detected: Suspected malicious content '{pattern}'")
            return True
    return False