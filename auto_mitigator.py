import sqlite3
import subprocess
import os
from datetime import datetime

class AutoMitigationEngine:
    def __init__(self, db_name="swarm_execution_memory.db"):
        self.db_name = db_name

    def trigger_voice_alert(self, message):
        try:
            subprocess.Popen(["termux-tts-speak", message], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass

    def execute_mitigation(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Fetch latest anomaly records
        cursor.execute("SELECT id, timestamp, temperature, vibration FROM sensor_telemetry WHERE status='CRITICAL_ANOMALY' ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()

        if row:
            rec_id, ts, temp, vib = row
            print(f"\n🚨 [AUTO-MITIGATOR ACTIVE] Anomaly Record Identified (ID: {rec_id})")
            print(f"📊 Telemetry Metrics: Temp: {temp}°C | Vibration: {vib} g")
            
            # Action 1: Emit TTS Voice Warning
            alert_msg = f"Critical Overheat Detected! Temperature {temp} degrees. Executing Auto Shutdown Protocol."
            print(f"🎙️ [Voice Alert]: {alert_msg}")
            self.trigger_voice_alert(alert_msg)

            # Action 2: Update Sensor Telemetry Record
            cursor.execute("UPDATE sensor_telemetry SET status='MITIGATED_SHUTDOWN' WHERE id=?", (rec_id,))

            # Action 3: Log Action to Swarm Execution Memory
            log_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute('''
                INSERT INTO task_history (task_description, category, status, result, timestamp)
                VALUES (?, ?, ?, ?, ?)
            ''', ("Predictive Maintenance Auto-Mitigation", "SYSTEM_CORE", "SUCCESS", f"Mitigated ID {rec_id} (Temp {temp}C)", log_time))

            conn.commit()
            print("✅ [ACTION COMPLETE] Record updated to MITIGATED_SHUTDOWN and logged to Task Memory.")
        else:
            print("\n🟢 [AUTO-MITIGATOR] No active unmitigated critical anomalies found.")

        conn.close()

if __name__ == "__main__":
    engine = AutoMitigationEngine()
    engine.execute_mitigation()
