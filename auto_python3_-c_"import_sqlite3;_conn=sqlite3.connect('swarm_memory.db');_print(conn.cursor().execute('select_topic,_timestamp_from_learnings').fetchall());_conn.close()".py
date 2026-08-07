import sqlite3
import os
import sys

def create_database():
    try:
        conn = sqlite3.connect('swarm_memory.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS learnings
                     (topic text, timestamp text)''')
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Error creating database: {e}")

def insert_into_database(topic, timestamp):
    try:
        conn = sqlite3.connect('swarm_memory.db')
        c = conn.cursor()
        c.execute("INSERT INTO learnings VALUES (?, ?)", (topic, timestamp))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Error inserting into database: {e}")

def retrieve_from_database():
    try:
        conn = sqlite3.connect('swarm_memory.db')
        c = conn.cursor()
        rows = c.execute('SELECT topic, timestamp FROM learnings').fetchall()
        conn.close()
        return rows
    except sqlite3.Error as e:
        print(f"Error retrieving from database: {e}")

def main():
    create_database()
    # insert_into_database('Python', '2022-01-01')
    # insert_into_database('Machine Learning', '2022-01-02')
    rows = retrieve_from_database()
    for row in rows:
        print(row)

if __name__ == "__main__":
    main()