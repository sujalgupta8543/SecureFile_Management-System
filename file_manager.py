from security import encrypt_data, decrypt_data, validate_input, detect_malware
import os
import time
import json

METADATA_FILE = "metadata.json"
OWNERSHIP_FILE = "ownership.json"
SHARED_FILE = "shared.json"

def load_json(filename):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return {}

def save_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f)

file_owner = load_json(OWNERSHIP_FILE)
shared_files = load_json(SHARED_FILE)
metadata = load_json(METADATA_FILE)

def write_file(filename, content):
    encrypted = encrypt_data(content)
    # Ensure subdirectory or naming convention for files to avoid path traversal
    safe_filename = os.path.basename(filename)
    with open(safe_filename, "wb") as f:
        f.write(encrypted)
    print(f"File {safe_filename} saved securely!")

def read_file(filename):
    safe_filename = os.path.basename(filename)
    if not os.path.exists(safe_filename):
        return "File not found!"
    with open(safe_filename, "rb") as f:
        data = f.read()
    decrypted = decrypt_data(data)
    return decrypted

def create_file(user, filename, content):
    # Security Checks
    if not validate_input(filename, 50) or not validate_input(content, 1000):
        return "Security Violation: Input too large."
    if detect_malware(content):
        return "Security Violation: Malware detected."

    file_owner[filename] = user
    metadata[filename] = {
        "owner": user,
        "size": len(content),
        "created": time.ctime()
    }

    write_file(filename, content)
    save_json(OWNERSHIP_FILE, file_owner)
    save_json(METADATA_FILE, metadata)
    return "Success"

def access_file(user, filename):
    if file_owner.get(filename) == user or user in shared_files.get(filename, []):
        return read_file(filename)
    else:
        return "Access Denied!"

def share_file(owner, filename, target_user):
    if file_owner.get(filename) == owner:
        if filename not in shared_files:
            shared_files[filename] = []
        if target_user not in shared_files[filename]:
            shared_files[filename].append(target_user)
            save_json(SHARED_FILE, shared_files)
        return f"File '{filename}' shared with {target_user}"
    else:
        return "Only owner can share file!"

def view_metadata(filename):
    return metadata.get(filename)

def get_user_files(user):
    accessible = []
    for fname, owner in file_owner.items():
        if owner == user or user in shared_files.get(fname, []):
            accessible.append(fname)
    return accessible

