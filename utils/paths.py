# utils/paths.py
import os
from pathlib import Path

APP_NAME = "LockBox"
BASE_DIR = Path.home() / f".{APP_NAME.lower()}"
ASSETS_DIR = Path(__file__).resolve().parents[1] / "assets"

def ensure_data_dirs():
    os.makedirs(BASE_DIR, exist_ok=True)
    os.makedirs(BASE_DIR / "backups", exist_ok=True)
    os.makedirs(BASE_DIR / "logs", exist_ok=True)

def salt_path():
    return BASE_DIR / "salt.bin"

def db_path():
    return BASE_DIR / "lockbox.db"
