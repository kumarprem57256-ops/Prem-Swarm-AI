import sqlite3
import json

class Database:
    def __init__(self, db_name="swarm.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.setup()

    def setup(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS swarm_memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent TEXT,
                input_data TEXT,
                output_data TEXT
            )
        ''')
        self.conn.commit()

    def log(self, agent, input_data, output_data):
        self.cursor.execute(
            "INSERT INTO swarm_memory (agent, input_data, output_data) VALUES (?, ?, ?)",
            (agent, str(input_data), str(output_data))
        )
        self.conn.commit()

class ResearchAgent:
    def __init__(self, db):
        self.db = db

    def execute(self, topic):
        result = f"[Research Summary]: High efficiency algorithms and multi-agent synergy for '{topic}'."
        self.db.log("ResearchAgent", topic, result)
        return result

class CoderAgent:
    def __init__(self, db):
        self.db = db

    def execute(self, spec):
        code = f"# Auto-generated code for: {spec}\ndef execute_task():\n    print('Prem Swarm Agent Executing: {spec}')\n\nexecute_task()"
        self.db.log("CoderAgent", spec, code)
        return code

class MediaAgent:
    def __init__(self, db):
        self.db = db

    def execute(self, topic):
        strategy = f"1. Hook: 'Unlocking {topic} with Autonomous AI'\n2. Demo: Live Execution Log\n3. Call to Action: Join Prem Swarm Network"
        self.db.log("MediaAgent", topic, strategy)
        return strategy

class MultilingualAgent:
    def __init__(self, db):
        self.db = db

    def translate(self, text, target_lang="Hinglish"):
        # Multi-language translation engine mapping
        translations = {
            "Hindi": f"[हिंदी अनुवाद]: {text} का मिशन सफलतापूर्वक पूरा हुआ!",
            "Hinglish": f"[Hinglish Summary]: {text} ka mission successfully execute ho gaya hai!",
            "English": f"[English Translation]: Mission execution completed for {text}.",
            "Bhojpuri": f"[Bhojpuri Summary]: {text} ke mission ekdam bawal tarike se poora ho gail!"
        }
        translated_output = translations.get(target_lang, f"[{target_lang} Output]: {text}")
        self.db.log("MultilingualAgent", f"{text} -> {target_lang}", translated_output)
        return translated_output
