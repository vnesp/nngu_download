import sqlite3

conn = sqlite3.connect('base.db')
cursor = conn.cursor()


def insert(table, record):
    cursor.execute(f"""
        INSERT OR IGNORE INTO {table}
            VALUES (?{',?' * (len(record) - 1)})
    """, record)


def insertmany(table, numFields, records):
    cursor.executemany(f"""
        INSERT OR IGNORE INTO {table}
            VALUES (?{',?' * (numFields - 1)})
    """, records)

def select(table, fields = '*'):
    if not isinstance(fields, list):
        fields = [fields]
    cursor.execute(f"""
        SELECT {','.join(fields)}
          FROM {table}
    """)
    return cursor.fetchall()


def flush():
    conn.commit()
