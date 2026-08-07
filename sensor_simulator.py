import time
import random
import json
import sqlite3
from datetime import datetime

class SensorDataSimulator:
    def __init__(self, db_name="swarm_execution_memory.db"):
        self.db_name = db_name
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sensor_telemetry (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                temperature REAL,
                vibration REAL,
                rpm REAL,
                status TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def generate_stream(self, cycles=10):
        print("\n🛰️ [SENSOR SIMULATION ENGINE] Streaming Telemetry Data...\n")
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        for i in range(1, cycles + 1):
            # Normal range telemetry
            temp = round(random.uniform(65.0, 85.0), 2)
            vib = round(random.uniform(0.1, 0.5), 2)
            rpm = round(random.uniform(1400, 1600), 2)
            status = "HEALTHY"

            # Injecting synthetic failure anomaly at iteration 7
            if i == 7:
                temp = round(random.uniform(110.0, 135.0), 2)  # Overheating
                vib = round(random.uniform(1.8, 3.5), 2)      # Extreme Vibration
                status = "CRITICAL_ANOMALY"

            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute('''
                INSERT INTO sensor_telemetry (timestamp, temperature, vibration, rpm, status)
                VALUES (?, ?, ?, ?, ?)
            ''', (ts, temp, vib, rpm, status))
            conn.commit()

            print(f"[{ts}] Cycle #{i:02d} | Temp: {temp}°C | Vib: {vib} g | RPM: {rpm} | Status: {status}")
            time.sleep(1)

        conn.close()
        print("\n✅ Simulation Stream Injection Complete. Data logged to Memory DB.")

if __name__ == "__main__":
    sim = SensorDataSimulator()
    sim.generate_stream(cycles=10)
