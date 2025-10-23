"""
Local FastAPI server used by the desktop launcher.

- Serves static files from ./public
- Exposes /api/meet endpoints for add/list entries, start/stop, record events and results.
- Uses a small SQLite-backed DB (db.py).
"""
import os
import logging
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from datetime import datetime, timezone
from dotenv import load_dotenv

# local modules - ensure these files are added to repo if not present
from logging_setup import setup_logging
from db import ensure_db, add_entry, list_entries, record_event, list_events, compute_results
from auth import require_api_key
from backup_manager import BackupManager

load_dotenv()

DB_PATH = os.getenv("DB_PATH", "data/time_machine.db")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
BACKUP_DIR = os.getenv("BACKUP_DIR", "backups")

setup_logging(logfile="logs/app.log", level=getattr(logging, LOG_LEVEL.upper(), logging.INFO))
logger = logging.getLogger(__name__)

ensure_db(DB_PATH)
backup_mgr = BackupManager(backup_dir=BACKUP_DIR, db_path=DB_PATH)

app = FastAPI(title="Time Machine Local Server")

origins = [
    "http://127.0.0.1:8000",
    "http://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

if os.path.isdir("public"):
    app.mount("/", StaticFiles(directory="public", html=True), name="public")
else:
    logger.warning("public/ directory not found; UI will not be served")

class EntryIn(BaseModel):
    name: str
    lane: int = 0
    heat: int = 0

class EventRecordIn(BaseModel):
    entry_id: int
    time: str = None
    type: str = "finish"

@app.get("/api/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.now(timezone.utc).isoformat()}

@app.get("/api/meet")
async def meet_info():
    entries = list_entries(DB_PATH)
    return {"summary": "Time Machine Local Meet", "entries": len(entries)}

@app.post("/api/meet/entries", status_code=201)
async def add_entry_endpoint(e: EntryIn, authorized: bool = Depends(require_api_key)):
    logger.info("Adding entry: %s lane=%s heat=%s", e.name, e.lane, e.heat)
    entry = add_entry(DB_PATH, e.name, e.lane, e.heat)
    backup_mgr.create_backup()
    return entry

@app.get("/api/meet/entries")
async def list_entries_endpoint():
    return list_entries(DB_PATH)

@app.post("/api/meet/start")
async def start_meet(authorized: bool = Depends(require_api_key)):
    start_time = datetime.now(timezone.utc).isoformat()
    logger.info("Meet started at %s", start_time)
    return {"status": "started", "start_time": start_time}

@app.post("/api/meet/stop")
async def stop_meet(authorized: bool = Depends(require_api_key)):
    stop_time = datetime.now(timezone.utc).isoformat()
    logger.info("Meet stopped at %s", stop_time)
    backup_mgr.create_backup()
    return {"status": "stopped", "stop_time": stop_time}

@app.post("/api/meet/event", status_code=201)
async def record_event_endpoint(ev: EventRecordIn, authorized: bool = Depends(require_api_key)):
    entries = list_entries(DB_PATH)
    if not any(en["id"] == ev.entry_id for en in entries):
        raise HTTPException(status_code=404, detail="Entry not found")
    timestamp = ev.time or datetime.now(timezone.utc).isoformat()
    rec = record_event(DB_PATH, ev.entry_id, timestamp, ev.type)
    logger.info("Recorded event: %s", rec)
    return rec

@app.get("/api/meet/events")
async def get_events_endpoint():
    return list_events(DB_PATH)

@app.get("/api/meet/results")
async def get_results_endpoint():
    results = compute_results(DB_PATH)
    return results
    # Return path to backup file or stream file in production
    backup = backup_mgr.create_backup()
    if backup:
        return {"backup_file": backup}
    raise HTTPException(status_code=500, detail="Backup failed")
