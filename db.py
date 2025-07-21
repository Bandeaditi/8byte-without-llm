import sqlite3
import os
from datetime import datetime

DB_PATH = "receipts.db"

# Create table if it doesn't exist
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS receipts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            vendor TEXT,
            date TEXT,
            amount REAL,
            currency TEXT,
            ocr_text TEXT,
            uploaded_at TEXT
        )
    """)
    conn.commit()
    conn.close()

# Save a receipt to DB
def save_receipt(filename, vendor, date, amount, currency, ocr_text):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO receipts (filename, vendor, date, amount, currency, ocr_text, uploaded_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (filename, vendor, date, amount, currency, ocr_text, datetime.now().isoformat()))
    conn.commit()
    conn.close()

# Fetch all receipts
def get_all_receipts():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM receipts ORDER BY uploaded_at DESC")
    data = cursor.fetchall()
    conn.close()
    return data
