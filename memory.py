import sqlite3

class MemoryCore:
    def __init__(self, db_name="swarm_memory.db"):
        self.db_name = db_name
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS learnings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT,
                error_log TEXT,
                solution TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

    def save_learning(self, topic, error_log, solution):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO learnings (topic, error_log, solution)
            VALUES (?, ?, ?)
        ''', (topic, error_log, solution))
        conn.commit()
        conn.close()
        print(f"🧠 [Self-Learning Core] Saved new learning/fix to memory for '{topic}'.")

    def recall_learnings(self, topic):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT solution FROM learnings WHERE topic LIKE ?", (f"%{topic}%",))
        rows = cursor.fetchall()
        conn.close()
        return [r[0] for r in rows]
