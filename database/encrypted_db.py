# database/encrypted_db.py
import sqlite3
import json
from pathlib import Path
from utils.paths import db_path
from crypto.aes_gcm import encrypt, decrypt
from crypto.key_derivation import derive_key
import datetime

DB_SCHEMA = """
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    url TEXT,
    username TEXT,
    secret_json TEXT,
    notes_json TEXT,
    tags TEXT,
    created_at TEXT,
    modified_at TEXT
);
"""

class EncryptedDB:
    def __init__(self, master_password: str):
        self.db_file = Path(db_path())
        self.key = derive_key(master_password)
        self._conn = sqlite3.connect(self.db_file)
        self._conn.execute(DB_SCHEMA)
        self._conn.commit()

    def close(self):
        self._conn.close()

    def add_item(self, title, url, username, secret_plain, notes_plain="", tags=""):
        secret_enc = encrypt(self.key, secret_plain.encode())
        notes_enc = encrypt(self.key, notes_plain.encode()) if notes_plain else None
        now = datetime.datetime.utcnow().isoformat()
        self._conn.execute(
            "INSERT INTO items (title,url,username,secret_json,notes_json,tags,created_at,modified_at) VALUES (?,?,?,?,?,?,?,?)",
            (title, url, username,
             json.dumps(secret_enc),
             json.dumps(notes_enc) if notes_enc else None,
             tags, now, now)
        )
        self._conn.commit()

    def update_item(self, item_id, title, url, username, secret_plain, notes_plain, tags):
        secret_enc = encrypt(self.key, secret_plain.encode())
        notes_enc = encrypt(self.key, notes_plain.encode()) if notes_plain else None
        now = datetime.datetime.utcnow().isoformat()
        self._conn.execute(
            "UPDATE items SET title=?,url=?,username=?,secret_json=?,notes_json=?,tags=?,modified_at=? WHERE id=?",
            (title, url, username, json.dumps(secret_enc),
             json.dumps(notes_enc) if notes_enc else None,
             tags, now, item_id)
        )
        self._conn.commit()

    def delete_item(self, item_id):
        self._conn.execute("DELETE FROM items WHERE id=?", (item_id,))
        self._conn.commit()

    def list_items(self, query=None):
        cur = self._conn.cursor()
        if query:
            q = f"%{query}%"
            cur.execute("SELECT id,title,url,username,secret_json,notes_json,tags,created_at,modified_at FROM items WHERE title LIKE ? OR url LIKE ? OR tags LIKE ?",
                        (q, q, q))
        else:
            cur.execute("SELECT id,title,url,username,secret_json,notes_json,tags,created_at,modified_at FROM items")
        rows = cur.fetchall()
        out = []
        for r in rows:
            secret = None
            notes = None
            try:
                if r[4]:
                    sec_obj = json.loads(r[4])
                    secret = decrypt(self.key, sec_obj["nonce"], sec_obj["ciphertext"]).decode()
                if r[5]:
                    nobj = json.loads(r[5])
                    notes = decrypt(self.key, nobj["nonce"], nobj["ciphertext"]).decode()
            except Exception:
                secret = "<decryption error>"
            out.append({
                "id": r[0],
                "title": r[1],
                "url": r[2],
                "username": r[3],
                "secret": secret,
                "notes": notes,
                "tags": r[6],
                "created_at": r[7],
                "modified_at": r[8]
            })
        return out
