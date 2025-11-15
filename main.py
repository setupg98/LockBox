# main.py
import sys
from PyQt6.QtWidgets import QApplication
from gui.login_window import LoginWindow
from utils.paths import ensure_data_dirs
from utils.logger import setup_logging

def main():
    setup_logging()
    ensure_data_dirs()
    app = QApplication(sys.argv)
    login = LoginWindow()
    login.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
