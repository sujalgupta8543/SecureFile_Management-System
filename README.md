🔐 Secure File Management System
A multi-layered secure file management web application built with Python (Flask) that implements real-world security principles including two-factor authentication, file encryption, access control, and threat detection.

📌 Project Overview
This system allows users to securely register, login with 2FA, and perform file operations (create, read, share, view metadata) — all with encryption and active security threat detection running in the background.
Built as part of CSE316 - Operating Systems Lab, Lovely Professional University.

✨ Features

🔑 Password Authentication — bcrypt-hashed passwords (no plaintext storage)
📱 Two-Factor Authentication (2FA) — TOTP-based OTP compatible with Google Authenticator
🔒 File Encryption — All files encrypted at rest using Fernet symmetric encryption
🛡️ Access Control — Only file owner or explicitly shared users can read a file
📤 File Sharing — Owner can grant access to specific users
📊 Metadata Viewing — See file owner, size, and creation timestamp
🚫 Buffer Overflow Detection — Rejects inputs exceeding safe length thresholds
🦠 Malware Detection — Scans content for dangerous patterns before saving
🗂️ Path Traversal Prevention — Filenames sanitized using os.path.basename()


🗂️ Project Structure
secure-file-system/
│
├── app.py              # Flask web app — routes and session management
├── auth.py             # Signup, login, TOTP 2FA logic
├── file_manager.py     # File create, read, share, metadata operations
├── security.py         # Encryption, malware detection, input validation
│
├── users.json          # Stores hashed passwords and TOTP secrets
├── metadata.json       # Stores file metadata (owner, size, created)
├── ownership.json      # Maps filenames to their owners
├── secret.key          # Fernet encryption key (auto-generated)
│
├── requirements.txt    # Python dependencies
├── vercel.json         # Vercel deployment config
└── templates/          # HTML templates (login, 2fa, dashboard)

⚙️ Installation & Setup
1. Clone the repository
bashgit clone https://github.com/your-username/secure-file-system.git
cd secure-file-system
2. Install dependencies
bashpip install -r requirements.txt
3. Run the application
bashpython app.py
4. Open in browser
http://localhost:5000

📦 Dependencies
flask
bcrypt
cryptography
python-dotenv
pyotp

🔐 How Security Works
LayerMechanismProtects Against1bcrypt password hashingCredential theft2TOTP Two-Factor AuthenticationAccount takeover3Pre-auth session stateSession fixation4Fernet file encryptionUnauthorized disk access5Ownership + sharing ACLPrivilege escalation6Input length validationBuffer overflow7Malware pattern scanningCode injection8os.path.basename() sanitizationPath traversal

🚀 Usage Guide

Sign Up → Enter username & password → Scan the QR code with Google Authenticator
Login → Enter credentials → Enter the 6-digit OTP from your Authenticator app
Create File → Enter filename + content → File is encrypted and saved
Read File → Enter filename → Decrypted content shown (only if you own or have access)
Share File → Enter filename + target username → They can now read the file
View Metadata → Enter filename → See owner, size, creation time


🌐 Deployment
Configured for Vercel deployment using vercel.json.
bashnpm install -g vercel
vercel
