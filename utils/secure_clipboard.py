# utils/secure_clipboard.py
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

class SecureClipboard:
    @staticmethod
    def copy(text: str, ttl: int = 10):
        clipboard = QApplication.clipboard()
        clipboard.setText(text)
        # schedule clear
        QTimer.singleShot(ttl * 1000, lambda: SecureClipboard._clear_if_matches(text))

    @staticmethod
    def _clear_if_matches(original):
        clipboard = QApplication.clipboard()
        try:
            if clipboard.text() == original:
                clipboard.clear(mode=clipboard.ClipboardMode.Clipboard)
        except Exception:
            pass
