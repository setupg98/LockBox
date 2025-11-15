# gui/components/add_edit_dialog.py
from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QTextEdit, QDialogButtonBox, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtGui import QIcon
from utils.paths import ASSETS_DIR
from gui.components.password_generator import PasswordGeneratorDialog

class AddEditDialog(QDialog):
    def __init__(self, parent=None, item=None):
        super().__init__(parent)
        self.setWindowTitle("Add / Edit Item")
        icon_path = ASSETS_DIR / "icons" / "lock_minimal.png"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))
        self.layout = QFormLayout()
        self.title = QLineEdit()
        self.url = QLineEdit()
        self.username = QLineEdit()
        self.secret = QLineEdit()
        self.notes = QTextEdit()
        self.tags = QLineEdit()
        # password generator button
        gen_btn = QPushButton("Generate")
        gen_btn.clicked.connect(self.on_generate)
        h = QHBoxLayout()
        h.addWidget(self.secret)
        h.addWidget(gen_btn)
        self.layout.addRow("Title", self.title)
        self.layout.addRow("URL", self.url)
        self.layout.addRow("Username", self.username)
        self.layout.addRow("Password", h)
        self.layout.addRow("Notes", self.notes)
        self.layout.addRow("Tags", self.tags)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        self.layout.addWidget(buttons)
        self.setLayout(self.layout)
        if item:
            self.title.setText(item.get("title",""))
            self.url.setText(item.get("url",""))
            self.username.setText(item.get("username",""))
            self.secret.setText(item.get("secret",""))
            self.notes.setPlainText(item.get("notes") or "")
            self.tags.setText(item.get("tags") or "")

    def on_generate(self):
        dlg = PasswordGeneratorDialog(self)
        if dlg.exec():
            self.secret.setText(dlg.generated_password())

    def values(self):
        return {
            "title": self.title.text().strip(),
            "url": self.url.text().strip(),
            "username": self.username.text().strip(),
            "secret": self.secret.text(),
            "notes": self.notes.toPlainText(),
            "tags": self.tags.text().strip()
        }
