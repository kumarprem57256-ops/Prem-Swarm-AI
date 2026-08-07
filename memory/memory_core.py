import sqlite3
import datetime
import os

class MemoryCore:
    def __init__(self, db_path="swarm_memory.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create table if not exists with updated schema
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS learnings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT,
                error_type TEXT,
                solution TEXT,
                timestamp DATETIME
            )
        ''')
        conn.commit()

        # Schema Migration Guard: Check if 'error_type' column exists
        cursor.execute("PRAGMA table_info(learnings)")
        columns = [col[1] for col in cursor.fetchall()]
        if "error_type" not in columns:
            cursor.execute("ALTER TABLE learnings ADD COLUMN error_type TEXT")
            conn.commit()
            
        conn.close()

    def save_learning(self, topic, error_type, solution):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO learnings (topic, error_type, solution, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (topic, error_type, solution, datetime.now() if hasattr(datetime, 'now') else datetime.datetime.now()))
        conn.commit()
        conn.close()
        print("🧠 [Memory Core] Mission learning successfully indexed into database.")
