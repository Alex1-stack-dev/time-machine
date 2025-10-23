import sqlite3
import threading
import os
from typing import List, Dict, Optional

_lock = threading.Lock()

def ensure_db(db_path: str):
    os.makedirs(os.path.dirname(db_path) or ".", exist_ok=True)
    with _lock:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        # entries table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            lane INTEGER DEFAULT 0,
            heat INTEGER DEFAULT 0
        )
        """)
        # events table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entry_id INTEGER NOT NULL,
            timestamp TEXT NOT NULL,
            type TEXT NOT NULL,
            FOREIGN KEY(entry_id) REFERENCES entries(id) ON DELETE CASCADE
        )
        """)
        conn.commit()
        conn.close()

def add_entry(db_path: str, name: str, lane: int = 0, heat: int = 0) -> Dict:
    with _lock:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("INSERT INTO entries (name, lane, heat) VALUES (?, ?, ?)", (name, lane, heat))
        entry_id = cur.lastrowid
        conn.commit()
        conn.close()
        return {"id": entry_id, "name": name, "lane": lane, "heat": heat}

def list_entries(db_path: str) -> List[Dict]:
    with _lock:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("SELECT id, name, lane, heat FROM entries ORDER BY id")
        rows = cur.fetchall()
        conn.close()
        return [{"id": r[0], "name": r[1], "lane": r[2], "heat": r[3]} for r in rows]

def record_event(db_path: str, entry_id: int, timestamp: str, ev_type: str = "finish") -> Dict:
    with _lock:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("INSERT INTO events (entry_id, timestamp, type) VALUES (?, ?, ?)", (entry_id, timestamp, ev_type))
        ev_id = cur.lastrowid
        conn.commit()
        conn.close()
        return {"id": ev_id, "entry_id": entry_id, "timestamp": timestamp, "type": ev_type}

def list_events(db_path: str) -> List[Dict]:
    with _lock:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("SELECT id, entry_id, timestamp, type FROM events ORDER BY id")
        rows = cur.fetchall()
        conn.close()
        return [{"id": r[0], "entry_id": r[1], "timestamp": r[2], "type": r[3]} for r in rows]

def compute_results(db_path: str) -> List[Dict]:
    # Returns simple sorted finishes; extend logic as needed
    with _lock:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("SELECT e.entry_id, e.timestamp FROM events e WHERE e.type = 'finish' ORDER BY e.timestamp")
        rows = cur.fetchall()
        results = []
        place = 1
        for entry_id, timestamp in rows:
            cur2 = conn.cursor()
            cur2.execute("SELECT id, name, lane, heat FROM entries WHERE id = ?", (entry_id,))
            r = cur2.fetchone()
            if r:
                results.append({"place": place, "entry": {"id": r[0], "name": r[1], "lane": r[2], "heat": r[3]}, "time": timestamp})
                place += 1
        conn.close()
        return results
