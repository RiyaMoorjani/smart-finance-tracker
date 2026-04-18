import sqlite3
import pandas as pd
from datetime import datetime

DB_NAME = "finance.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            type TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            note TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_transaction(date, type_, category, amount, note=""):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "INSERT INTO transactions (date, type, category, amount, note) VALUES (?, ?, ?, ?, ?)",
        (date, type_, category, amount, note)
    )
    conn.commit()
    conn.close()

def get_all_transactions():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM transactions ORDER BY date DESC", conn)
    conn.close()
    return df

def delete_transaction(tid):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM transactions WHERE id = ?", (tid,))
    conn.commit()
    conn.close()

def get_monthly_summary(year, month):
    conn = sqlite3.connect(DB_NAME)
    query = f"""
        SELECT type, category, SUM(amount) as total
        FROM transactions
        WHERE strftime('%Y', date) = '{year}' AND strftime('%m', date) = '{month:02d}'
        GROUP BY type, category
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df
