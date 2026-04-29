import bcrypt
import json
import os
import pyotp

def get_path(filename):
    try:
        return filename if os.access(".", os.W_OK) else os.path.join("/tmp", filename)
    except:
        return os.path.join("/tmp", filename)

USER_DB = get_path("users.json")
def load_users():
    users = {}
    if os.path.exists("users.json"):
        with open("users.json", "r") as f:
            try: users.update(json.load(f))
            except: pass
    if USER_DB != "users.json" and os.path.exists(USER_DB):
        with open(USER_DB, "r") as f:
            try: users.update(json.load(f))
            except: pass
    return users

def save_users(users):
    with open(USER_DB, "w") as f:
        json.dump(users, f)

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

def signup(username, password):
    users = load_users()
    if username in users:
        return False
    # Generate a unique TOTP secret for the user
    totp_secret = pyotp.random_base32()
    users[username] = {
        "password": hash_password(password),
        "totp_secret": totp_secret
    }
    save_users(users)
    print(f"User {username} registered with TOTP secret!")
    return True

def login(username, password):
    users = load_users()
    if username in users:
        user_data = users[username]
        hashed = user_data["password"] if isinstance(user_data, dict) else user_data
        if check_password(password, hashed):
            # If migrating from old format, add a TOTP secret now
            if not isinstance(user_data, dict) or "totp_secret" not in user_data:
                totp_secret = pyotp.random_base32()
                if not isinstance(user_data, dict):
                    users[username] = {"password": hashed, "totp_secret": totp_secret}
                else:
                    users[username]["totp_secret"] = totp_secret
                save_users(users)
            
            print(f"Login successful for {username}!")
            return True
    return False

def get_totp_secret(username):
    users = load_users()
    user_data = users[username]
    return user_data.get("totp_secret")

def get_totp_uri(username):
    secret = get_totp_secret(username)
    if not secret:
        return None
    return pyotp.totp.TOTP(secret).provisioning_uri(name=username, issuer_name="SecureFS")

def verify_totp(username, code):
    secret = get_totp_secret(username)
    if not secret:
        return False
    totp = pyotp.TOTP(secret)
    # Allows a small window for clock drift
    if totp.verify(code):
        print(f"TOTP 2FA successful for {username}!")
        return True
    return False

