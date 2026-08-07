import sqlite3

def run_pdm_analysis():
    conn = sqlite3.connect("swarm_execution_memory.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sensor_telemetry ORDER BY id DESC LIMIT 10")
    rows = cursor.fetchall()
    
    print("\n🧠 [PREDICTIVE MAINTENANCE AGENT] Running Neural Anomaly Scan...\n")
    anomalies_detected = 0
    
    for row in reversed(rows):
        _, ts, temp, vib, rpm, status = row
        if temp > 100 or vib > 1.2:
            print(f"🚨 [ALERT DETECTED at {ts}] Temp: {temp}°C, Vib: {vib} g -> ACTION: AUTO-SHUTDOWN DIRECTIVE PENDING")
            anomalies_detected += 1
        else:
            print(f"🟢 [NORMAL RANGE at {ts}] Temp: {temp}°C, Vib: {vib} g -> SYSTEM HEALTHY")

    conn.close()
    print(f"\n📊 Summary: Total Anomalies Isolated = {anomalies_detected}")

if __name__ == "__main__":
    run_pdm_analysis()
