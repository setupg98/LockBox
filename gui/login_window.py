# gui/login_window.py
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PyQt6.QtGui import QIcon
from gui.main_window import MainWindow
from database.encrypted_db import EncryptedDB
from utils.paths import db_path
import os
from utils.paths import ASSETS_DIR

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LockBox — Unlock")
        # set app icon (3D shield)
        icon_path = ASSETS_DIR / "icons" / "shield_3d.png"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))
        self.resize(420, 260)
        self.layout = QVBoxLayout()
        self.lbl = QLabel("Enter master password (first run: create one)")
        self.pass_edit = QLineEdit()
        self.pass_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.btn = QPushButton("Unlock / Create")
        self.btn.clicked.connect(self.on_unlock)
        self.layout.addWidget(self.lbl)
        self.layout.addWidget(self.pass_edit)
        self.layout.addWidget(self.btn)
        self.setLayout(self.layout)

    def on_unlock(self):
        mp = self.pass_edit.text().strip()
        if not mp or len(mp) < 6:
            QMessageBox.warning(self, "Weak password", "Master password must be at least 6 characters.")
            return
        # Attempt to open DB - if db exists, this will verify by listing items (decryption)
        try:
            db = EncryptedDB(mp)
            # quick test: list items to ensure derivation works (if corruption / salt mismatch will error)
            _ = db.list_items()
        except Exception as e:
            QMessageBox.critical(self, "Error unlocking", f"Failed to unlock or init database:\n{e}")
            return
        self.main = MainWindow(db, mp)
        self.main.show()
        self.close()
