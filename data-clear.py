import sqlite3
import re

DATABASE = '/nfs/demo.db'

def connect_db():
    return sqlite3.connect(DATABASE)

def is_junk_task(description):
    junk_keywords = [
        'alert(', '<script', '<a>', '%3c', '%3e', '</', '/>', '><', '--', 'UNION', 'SELECT', 'sqlmap', 'Arachni',
        'cgAhLG', 'nwtbe', 'wuh77', 'yh380', 'dv5na'
    ]
    for keyword in junk_keywords:
        if keyword.lower() in description.lower():
            return True

    if re.fullmatch(r'[a-z0-9]{5,10}', description):
        return True

    return False

def clear_junk_tasks():
    db = connect_db()
    cursor = db.cursor()

    cursor.execute("SELECT id, description FROM tasks")
    rows = cursor.fetchall()

    junk_ids = [row[0] for row in rows if is_junk_task(row[1])]

    for junk_id in junk_ids:
        cursor.execute("DELETE FROM tasks WHERE id = ?", (junk_id,))
    db.commit()

    print(f"Deleted {len(junk_ids)} junk/fuzzed tasks.")
    db.close()

if __name__ == '__main__':
    clear_junk_tasks()
