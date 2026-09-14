import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "finance.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    amount REAL NOT NULL,
    description TEXT,
    category TEXT,
    source TEXT NOT NULL,
    account TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS debts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    principal REAL NOT NULL,
    current_balance REAL NOT NULL,
    interest_rate REAL,
    due_date TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS debt_payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    debt_id INTEGER NOT NULL REFERENCES debts(id),
    date TEXT NOT NULL,
    amount REAL NOT NULL,
    note TEXT
);

CREATE TABLE IF NOT EXISTS categories (
    name TEXT PRIMARY KEY,
    type TEXT NOT NULL
);
"""

def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    conn = get_connection()
    conn.executescript(SCHEMA)
    conn.commit()
    conn.close()
    print(f"Database initialized at {DB_PATH}")

DEFAULT_CATEGORIES = [
    ("Food & Dining", "expense"),
    ("Transport", "expense"),
    ("Shopping", "expense"),
    ("Rent", "expense"),
    ("Utilities", "expense"),
    ("Entertainment", "expense"),
    ("Health", "expense"),
    ("Groceries", "expense"),
    ("Salary", "income"),
    ("Other Income", "income"),
    ("Uncategorized", "expense"),
]

def seed_categories():
    conn = get_connection()
    cur = conn.cursor()
    for name, type_ in DEFAULT_CATEGORIES:
        cur.execute(
            "INSERT OR IGNORE INTO categories (name, type) VALUES (?, ?)",
            (name, type_)
        )
    conn.commit()
    conn.close()
    print(f"Seeded {len(DEFAULT_CATEGORIES)} categories")
    
if __name__ == "__main__":
    init_db()
    seed_categories()