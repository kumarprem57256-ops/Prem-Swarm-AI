import sqlite3

def run_task():
    conn = sqlite3.connect("swarm_execution_memory.db")
    cursor = conn.cursor()
    
    # Extract Tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [t[0] for t in cursor.fetchall()]
    
    print("\n📊 [SWARM DATABASE NATIVE SUMMARY]")
    print("=" * 45)
    print(f"Total Tables Found: {len(tables)}")
    print(f"Tables: {', '.join(tables)}")
    print("-" * 45)

    # Extract Row Counts
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"📌 Table '{table}': {count} records logged.")

    conn.close()
    print("=" * 45 + "\n")

if __name__ == "__main__":
    run_task()
