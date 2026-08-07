import sqlite3
import json
from datetime import datetime

class SwarmMemory:
    def __init__(self, db_name="swarm_memory.db"):
        self.db_name = db_name
        self._init_db()

    def _init_db(self):
        """Database aur tables initialize karta hai agar exist na karte ho."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memory_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                agent_id TEXT NOT NULL,
                mission TEXT NOT NULL,
                status TEXT NOT NULL,
                output TEXT
            )
        ''')
        
        conn.commit()
        conn.close()

    def add_log(self, agent_id, mission, status="Completed", output=""):
        """Nayi memory entry database mein save karta hai."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        cursor.execute('''
            INSERT INTO memory_logs (timestamp, agent_id, mission, status, output)
            VALUES (?, ?, ?, ?, ?)
        ''', (timestamp, agent_id, mission, status, str(output)))
        
        conn.commit()
        conn.close()
        print(f"[MEMORY DB SAVED] Log stored for '{agent_id}' at {timestamp}")

    def fetch_all_logs(self):
        """Sabhi stored memory logs fetch karke display karta hai."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, timestamp, agent_id, mission, status FROM memory_logs')
        rows = cursor.fetchall()
        conn.close()
        return rows

if __name__ == "__main__":
    mem = SwarmMemory()
    mem.add_log("System_Test", "Database Verification", "Success", "Test Output")
    print("\n--- Current DB Logs ---")
    for log in mem.fetch_all_logs():
        print(log)
