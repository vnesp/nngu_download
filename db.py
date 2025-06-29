import sqlite3

conn = sqlite3.connect('base.db')
cursor = conn.cursor()

def insert(table, record):
    cursor.execute(f"""
        INSERT OR IGNORE INTO {table}
            VALUES (?{',?' * (len(record) - 1)})
    """, record)

def flush():
    conn.commit()