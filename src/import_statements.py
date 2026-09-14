import pandas as pd
from db import get_connection

def import_csv(filepath, account="Default", source="bank_csv"):
    df = pd.read_csv(filepath)
    conn = get_connection()
    cur = conn.cursor()

    for _, row in df.iterrows():
        cur.execute(
            """INSERT INTO transactions (date, amount, description, source, account)
               VALUES (?, ?, ?, ?, ?)""",
            (row["date"], row["amount"], row["description"], source, account)
        )

    conn.commit()
    print(f"Imported {len(df)} transactions from {filepath}")
    conn.close()

if __name__ == "__main__":
    import_csv("../raw_statements/sample.csv")