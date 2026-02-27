import sqlite3

with open('schema_utf8.txt', 'w', encoding='utf-8') as f:
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    # Get table schema
    cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='tracker_progress';")
    f.write("Schema:\n")
    f.write(str(cursor.fetchone()[0]) + "\n")

    # Get column info
    cursor.execute("PRAGMA table_info(tracker_progress);")
    f.write("\nColumns:\n")
    for row in cursor.fetchall():
        f.write(str(row) + "\n")
