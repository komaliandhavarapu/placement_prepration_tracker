import sqlite3

c = sqlite3.connect('db.sqlite3')
print("tracker_codingattempt schema:")
for row in c.execute("PRAGMA table_info(tracker_codingattempt)"):
    print(row)

print("tracker_codingquestion schema:")
for row in c.execute("PRAGMA table_info(tracker_codingquestion)"):
    print(row)

print("Cleaning...")
c.execute('PRAGMA foreign_keys = OFF')
c.execute('DROP TABLE IF EXISTS tracker_codingattempt')
c.execute('DROP TABLE IF EXISTS tracker_codingquestion')
c.execute("DELETE FROM django_migrations WHERE app='tracker' AND name='0006_codingquestion_codingattempt'")
c.commit()
c.close()
print("Done")
