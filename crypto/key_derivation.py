# crypto/key_derivation.py
import os
from argon2.low_level import hash_secret_raw, Type
from pathlib import Path
from utils.paths import salt_path
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

def load_or_create_salt():
    p = Path(salt_path())
    if not p.exists():
        p.parent.mkdir(parents=True, exist_ok=True)
        s = os.urandom(16)
        p.write_bytes(s)
        return s
    return p.read_bytes()

def derive_key(master_password: str, length: int = 32) -> bytes:
    """
    Derive a binary key from master password using Argon2id then HKDF to get desired length.
    """
    salt = load_or_create_salt()
    # Argon2id raw output
    raw = hash_secret_raw(
        secret=master_password.encode('utf-8'),
        salt=salt,
        time_cost=3,
        memory_cost=64 * 1024,  # 64 MiB
        parallelism=2,
        hash_len=32,
        type=Type.ID
    )
    # HKDF to expand / mix
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=length,
        salt=None,
        info=b"lockbox-key-derivation"
    )
    return hkdf.derive(raw)
