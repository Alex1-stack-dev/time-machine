import sqlite3
from datetime import datetime
from contextlib import contextmanager

class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        with self.get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS races (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    date TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS results (
                    id INTEGER PRIMARY KEY,
                    race_id INTEGER,
                    place INTEGER,
                    name TEXT NOT NULL,
                    time TEXT NOT NULL,
                    heat INTEGER,
                    dq BOOLEAN DEFAULT FALSE,
                    FOREIGN KEY (race_id) REFERENCES races (id)
                )
            """)
    
    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()
    
    def save_race_results(self, race_name, results):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO races (name, date) VALUES (?, ?)",
                (race_name, datetime.now().isoformat())
            )
            race_id = cursor.lastrowid
            
            for result in results:
                cursor.execute("""
                    INSERT INTO results (race_id, place, name, time, heat, dq)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (race_id, result.place, result.name, result.time, 
                     result.heat, bool(result.dq)))
