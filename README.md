# 🔐 Password Wallet with Face Authentication

A desktop application built using Python's Tkinter for managing your passwords securely with face recognition authentication.

## 📦 Features

- Face-based login using webcam
- Encrypted password autofill
- Password manager with CRUD (Insert, Update, Delete)
- Strong password generator
- MySQL database for data storage

## 🚀 Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/PasswordWallet-FaceAuth.git
cd PasswordWallet-FaceAuth
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up MySQL
- Install MySQL Server
- Set user to `root` with no password (or update `Password_wallet.py` if using different credentials)
- Database and tables will be created automatically on first run.

### 4. Run the App
```bash
python Password_wallet.py
```

## 📂 Folder Notes

- `faces/`: Store registered face images here (auto-created during sign up).
- `test.png`: Temporarily used for capturing login face (auto-generated).
- Make sure you have a working webcam for face recognition.

## 📸 Face Recognition

Uses the `face_recognition` library to match faces using encodings. Recommended lighting and front-facing images for best accuracy.

---

Made with ❤️ using Python & OpenCV
