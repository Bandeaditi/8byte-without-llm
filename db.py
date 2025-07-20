import sqlite3

def init_db():
    conn = sqlite3.connect("receipts.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS receipts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vendor TEXT,
        date TEXT,
        amount REAL,
        category TEXT
    )''')
    conn.commit()
    conn.close()

def insert_receipt(data):
    conn = sqlite3.connect("receipts.db")
    c = conn.cursor()
    c.execute("INSERT INTO receipts (vendor, date, amount, category) VALUES (?, ?, ?, ?)",
              (data['vendor'], data['date'], data['amount'], data['category']))
    conn.commit()
    conn.close()

def get_all_receipts():
    conn = sqlite3.connect("receipts.db")
    df = conn.cursor().execute("SELECT * FROM receipts").fetchall()
    conn.close()
    return df
