import pyodbc

SERVER = r"localhost\SQLEXPRESS"
DATABASE = "FinanceManagerDB"

CONN_STRING = (
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    f"Trusted_Connection=yes;"
    f"TrustServerCertificate=yes;"
)

SCHEMA_STATEMENTS = [
    """
    IF OBJECT_ID('transactions', 'U') IS NULL
    CREATE TABLE transactions (
        id INT IDENTITY(1,1) PRIMARY KEY,
        date DATE NOT NULL,
        amount FLOAT NOT NULL,
        description NVARCHAR(255),
        category NVARCHAR(100),
        source NVARCHAR(50) NOT NULL,
        account NVARCHAR(100),
        created_at DATETIME DEFAULT GETDATE()
    )
    """,
    """
    IF OBJECT_ID('debts', 'U') IS NULL
    CREATE TABLE debts (
        id INT IDENTITY(1,1) PRIMARY KEY,
        name NVARCHAR(100) NOT NULL,
        type NVARCHAR(20) NOT NULL,
        principal FLOAT NOT NULL,
        current_balance FLOAT NOT NULL,
        interest_rate FLOAT,
        due_date DATE,
        created_at DATETIME DEFAULT GETDATE()
    )
    """,
    """
    IF OBJECT_ID('debt_payments', 'U') IS NULL
    CREATE TABLE debt_payments (
        id INT IDENTITY(1,1) PRIMARY KEY,
        debt_id INT NOT NULL FOREIGN KEY REFERENCES debts(id),
        date DATE NOT NULL,
        amount FLOAT NOT NULL,
        note NVARCHAR(255)
    )
    """,
    """
    IF OBJECT_ID('categories', 'U') IS NULL
    CREATE TABLE categories (
        name NVARCHAR(100) PRIMARY KEY,
        type NVARCHAR(20) NOT NULL
    )
    """
]

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

def get_connection():
    return pyodbc.connect(CONN_STRING)

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    for stmt in SCHEMA_STATEMENTS:
        cur.execute(stmt)
    conn.commit()
    conn.close()
    print("Database schema initialized")

def seed_categories():
    conn = get_connection()
    cur = conn.cursor()
    for name, type_ in DEFAULT_CATEGORIES:
        cur.execute(
            """IF NOT EXISTS (SELECT 1 FROM categories WHERE name = ?)
               INSERT INTO categories (name, type) VALUES (?, ?)""",
            (name, name, type_)
        )
    conn.commit()
    conn.close()
    print(f"Seeded {len(DEFAULT_CATEGORIES)} categories")

if __name__ == "__main__":
    init_db()
    seed_categories()