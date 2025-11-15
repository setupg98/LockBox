# utils/logger.py
import logging
from pathlib import Path
from .paths import BASE_DIR

def setup_logging():
    log_dir = Path(BASE_DIR) / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    fh = logging.FileHandler(log_dir / "app.log", encoding="utf-8")
    fmt = "%(asctime)s %(levelname)s %(name)s %(message)s"
    logging.basicConfig(level=logging.INFO, format=fmt, handlers=[fh])
