# gui/components/password_generator.py
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QCheckBox, QPushButton
import secrets, string

class PasswordGeneratorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Password Generator")
        self.layout = QVBoxLayout()
        row = QHBoxLayout()
        row.addWidget(QLabel("Length:"))
        self.len_spin = QSpinBox()
        self.len_spin.setRange(8, 64)
        self.len_spin.setValue(16)
        row.addWidget(self.len_spin)
        self.chk_upper = QCheckBox("Upper")
        self.chk_upper.setChecked(True)
        self.chk_lower = QCheckBox("Lower")
        self.chk_lower.setChecked(True)
        self.chk_digits = QCheckBox("Digits")
        self.chk_digits.setChecked(True)
        self.chk_symbols = QCheckBox("Symbols")
        self.chk_symbols.setChecked(True)
        self.layout.addLayout(row)
        self.layout.addWidget(self.chk_upper)
        self.layout.addWidget(self.chk_lower)
        self.layout.addWidget(self.chk_digits)
        self.layout.addWidget(self.chk_symbols)
        gen_btn = QPushButton("Generate")
        gen_btn.clicked.connect(self.accept)
        self.layout.addWidget(gen_btn)
        self.setLayout(self.layout)
        self._password = ""

    def accept(self):
        chars = ""
        if self.chk_lower.isChecked():
            chars += string.ascii_lowercase
        if self.chk_upper.isChecked():
            chars += string.ascii_uppercase
        if self.chk_digits.isChecked():
            chars += string.digits
        if self.chk_symbols.isChecked():
            chars += "!@#$%^&*()-_=+[]{};:,.<>/?"
        if not chars:
            chars = string.ascii_letters + string.digits
        length = self.len_spin.value()
        self._password = "".join(secrets.choice(chars) for _ in range(length))
        super().accept()

    def generated_password(self):
        return self._password
