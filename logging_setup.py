import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logging(logfile="logs/app.log", level=logging.INFO):
    os.makedirs(os.path.dirname(logfile) or ".", exist_ok=True)
    logger = logging.getLogger()
    logger.setLevel(level)

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    ch.setFormatter(ch_formatter)

    # Rotating file handler
    fh = RotatingFileHandler(logfile, maxBytes=5 * 1024 * 1024, backupCount=5, encoding="utf-8")
    fh.setLevel(level)
    fh_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    fh.setFormatter(fh_formatter)

    # Avoid duplicate handlers
    if not logger.handlers:
        logger.addHandler(ch)
        logger.addHandler(fh)
    else:
        # replace existing handlers for consistent formatting
        logger.handlers = [ch, fh]

    # Less verbose third-party libraries
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)
