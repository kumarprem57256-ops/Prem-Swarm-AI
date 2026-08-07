import sqlite3
import sys

DB_NAME = "swarm_memory.db"

def show_menu():
    print("\n========================================")
    print("    PREM SWARM AI: DATABASE VIEWER      ")
    print("========================================")
    print("1. View All Memory Logs (Summary)")
    print("2. Filter Logs by Agent ID")
    print("3. View Full Output by Log ID")
    print("4. Exit")
    print("========================================")

def view_all_logs():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT id, timestamp, agent_id, mission, status FROM memory_logs ORDER BY id DESC')
    rows = cursor.fetchall()
    conn.close()

    print("\n--- ALL MEMORY LOGS (Latest First) ---")
    if not rows:
        print("No logs found in database.")
        return
    for r in rows:
        print(f"[ID: {r[0]}] | {r[1]} | Agent: {r[2]} | Status: {r[4]}")
        print(f"  Mission: {r[3]}\n")

def filter_by_agent():
    agent_id = input("\nEnter Agent ID (e.g. Agent_01_Media, Agent_02_Researcher, Agent_03_Coder): ").strip()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT id, timestamp, agent_id, mission, status FROM memory_logs WHERE agent_id LIKE ? ORDER BY id DESC', (f"%{agent_id}%",))
    rows = cursor.fetchall()
    conn.close()

    print(f"\n--- LOGS FOR '{agent_id}' ---")
    if not rows:
        print("No matching logs found.")
        return
    for r in rows:
        print(f"[ID: {r[0]}] | {r[1]} | Status: {r[4]}")
        print(f"  Mission: {r[3]}\n")

def view_full_output():
    log_id = input("\nEnter Log ID to inspect output: ").strip()
    if not log_id.isdigit():
        print("Invalid ID.")
        return
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT id, timestamp, agent_id, mission, status, output FROM memory_logs WHERE id = ?', (int(log_id),))
    row = cursor.fetchone()
    conn.close()

    if not row:
        print("Log ID not found.")
        return

    print("\n========================================")
    print(f" LOG DETAILS [ID: {row[0]}]")
    print("========================================")
    print(f"Time   : {row[1]}")
    print(f"Agent  : {row[2]}")
    print(f"Status : {row[4]}")
    print(f"Mission: {row[3]}")
    print("\n--- FULL OUTPUT DATA ---")
    print(row[5])
    print("========================================\n")

def main():
    while True:
        show_menu()
        choice = input("Enter choice (1-4): ").strip()
        if choice == '1':
            view_all_logs()
        elif choice == '2':
            filter_by_agent()
        elif choice == '3':
            view_full_output()
        elif choice == '4':
            print("Exiting Database Viewer.")
            sys.exit(0)
        else:
            print("Invalid option! Try again.")

if __name__ == "__main__":
    main()
