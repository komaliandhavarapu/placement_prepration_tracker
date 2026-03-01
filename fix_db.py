import sqlite3

def fix():
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS tracker_codingquestion')
    c.execute('DROP TABLE IF EXISTS tracker_codingattempt')
    c.execute("DELETE FROM django_migrations WHERE app='tracker' AND name='0006_codingquestion_codingattempt'")
    conn.commit()
    conn.close()
    print("Fixed!")

if __name__ == '__main__':
    fix()
