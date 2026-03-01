import sqlite3

c = sqlite3.connect('db.sqlite3')
print("All tables:")
for row in c.execute("SELECT name FROM sqlite_master WHERE type='table'"):
    print(row[0])

# Check what columns exist in any tracker_coding* table
for row in c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%coding%'"):
    tname = row[0]
    print(f"Schema for {tname}:")
    for r in c.execute(f"PRAGMA table_info({tname})"):
        print(r)
