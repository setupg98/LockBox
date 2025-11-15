# gui/main_window.py
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QLineEdit, QLabel, QMessageBox
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import QTimer
from gui.components.add_edit_dialog import AddEditDialog
from exporters.export_xlsx import export_items_to_xlsx
from utils.secure_clipboard import SecureClipboard
from utils.paths import ASSETS_DIR
import tempfile
import os

class MainWindow(QMainWindow):
    def __init__(self, db, master_password):
        super().__init__()
        self.db = db
        self.master_password = master_password
        self.setWindowTitle("LockBox — Dashboard")
        icon_path = ASSETS_DIR / "icons" / "shield_3d.png"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))
        self.resize(1000, 600)
        self._build_ui()
        self.load_items()
        # autolock timer (5 min)
        self.autolock_timer = QTimer()
        self.autolock_timer.setInterval(5 * 60 * 1000)
        self.autolock_timer.timeout.connect(self.lock)
        self.autolock_timer.start()

    def _build_ui(self):
        w = QWidget()
        h = QHBoxLayout()
        # Left sidebar (icons)
        sidebar = QVBoxLayout()
        add_btn = QPushButton("➕ Add")
        add_btn.clicked.connect(self.on_add)
        import_btn = QPushButton("📥 Import CSV")
        import_btn.clicked.connect(self.on_import)
        export_btn = QPushButton("📤 Export XLSX")
        export_btn.clicked.connect(self.on_export)
        sidebar.addWidget(add_btn)
        sidebar.addWidget(import_btn)
        sidebar.addWidget(export_btn)
        sidebar.addStretch()
        # Main area
        area = QVBoxLayout()
        search_row = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search title, url, tags...")
        self.search_input.returnPressed.connect(self.on_search)
        search_row.addWidget(QLabel("Search:"))
        search_row.addWidget(self.search_input)
        area.addLayout(search_row)
        # Table
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["ID", "Title", "Username", "URL", "Tags"])
        self.table.cellDoubleClicked.connect(self.on_table_double)
        area.addWidget(self.table)
        h.addLayout(sidebar, 1)
        h.addLayout(area, 6)
        w.setLayout(h)
        self.setCentralWidget(w)
        # Menus
        menubar = self.menuBar()
        file_menu = menubar.addMenu("&File")
        lock_action = QAction("Lock", self)
        lock_action.triggered.connect(self.lock)
        file_menu.addAction(lock_action)
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def load_items(self, query=None):
        items = self.db.list_items(query)
        self.table.setRowCount(len(items))
        for r, it in enumerate(items):
            self.table.setItem(r, 0, QTableWidgetItem(str(it["id"])))
            self.table.setItem(r, 1, QTableWidgetItem(it["title"]))
            self.table.setItem(r, 2, QTableWidgetItem(it["username"]))
            self.table.setItem(r, 3, QTableWidgetItem(it["url"]))
            self.table.setItem(r, 4, QTableWidgetItem(it["tags"] or ""))

    def on_add(self):
        dlg = AddEditDialog(parent=self)
        if dlg.exec():
            data = dlg.values()
            self.db.add_item(data["title"], data["url"], data["username"], data["secret"], data["notes"], data["tags"])
            self.load_items()

    def on_table_double(self, row, col):
        item_id = int(self.table.item(row, 0).text())
        # fetch item by id (simple)
        items = [i for i in self.db.list_items() if i["id"] == item_id]
        if not items:
            QMessageBox.warning(self, "Not found", "Item not found")
            return
        it = items[0]
        dlg = AddEditDialog(parent=self, item=it)
        if dlg.exec():
            d = dlg.values()
            self.db.update_item(item_id, d["title"], d["url"], d["username"], d["secret"], d["notes"], d["tags"])
            self.load_items()

    def on_search(self):
        q = self.search_input.text().strip()
        self.load_items(query=q if q else None)

    def on_export(self):
        items = self.db.list_items()
        tmp = tempfile.gettempdir()
        dest = os.path.join(tmp, "lockbox_export.xlsx")
        export_items_to_xlsx(items, dest)
        QMessageBox.information(self, "Exported", f"Exported to {dest}")

    def on_import(self):
        QMessageBox.information(self, "Import", "CSV import wizard not yet implemented in MVP.")

    def lock(self):
        # close DB and go back to login
        self.db.close()
        from gui.login_window import LoginWindow
        self.hide()
        self.login = LoginWindow()
        self.login.show()
        self.close()

    def copy_secret_to_clipboard(self, secret: str, ttl_seconds: int = 10):
        SecureClipboard.copy(secret, ttl_seconds)
