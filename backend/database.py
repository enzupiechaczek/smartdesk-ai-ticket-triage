import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "smartdesk.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_connection() as conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject TEXT NOT NULL,
                description TEXT NOT NULL,
                category TEXT NOT NULL,
                confidence REAL NOT NULL,
                priority TEXT NOT NULL,
                created_at TEXT NOT NULL
            )"""
        )