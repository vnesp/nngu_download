import sqlite3

conn = sqlite3.connect('base.db')
cursor = conn.cursor()


def insert(table, record):
    cursor.execute("""
        INSERT OR IGNORE INTO {}
            VALUES (?{})
    """.format(table, ',?' * (len(record) - 1)), record)


def insertmany(table, numFields, records):
    cursor.executemany("""
        INSERT OR IGNORE INTO {}
            VALUES (?{})
    """.format(table, ',?' * (numFields - 1)), records)

def select(table, fields = '*'):
    if not isinstance(fields, list):
        fields = [fields]
    cursor.execute("""
        SELECT {}
          FROM {}
    """.format(','.join(fields), table))
    return cursor.fetchall()


def flush():
    conn.commit()
