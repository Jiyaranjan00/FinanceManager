import re
from db import get_connection

# keyword -> category mapping. Keywords are matched case-insensitively
# against the transaction description. Order matters: first match wins.
RULES = {
    "Food & Dining": ["swiggy", "zomato", "restaurant", "cafe", "dominos", "mcdonald"],
    "Transport": ["uber", "ola", "rapido", "petrol", "fuel", "metro", "irctc"],
    "Groceries": ["bigbasket", "blinkit", "zepto", "grofers", "dmart"],
    "Shopping": ["amazon", "flipkart", "myntra", "ajio"],
    "Rent": ["rent payment", "rent"],
    "Utilities": ["electricity", "recharge", "broadband", "wifi", "gas bill"],
    "Entertainment": ["netflix", "spotify", "prime video", "hotstar", "movie", "bookmyshow"],
    "Health": ["pharmacy", "hospital", "clinic", "medplus", "apollo"],
    "Salary": ["salary credit", "salary"],
}

def categorize_description(description):
    """Return the best-matching category for a transaction description,
    or 'Uncategorized' if no rule matches."""
    desc_lower = description.lower()
    for category, keywords in RULES.items():
        for kw in keywords:
            if kw in desc_lower:
                return category
    return "Uncategorized"

def categorize_all_uncategorized():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, description FROM transactions WHERE category IS NULL")
    rows = cur.fetchall()

    updated = 0
    for txn_id, description in rows:
        category = categorize_description(description or "")
        cur.execute(
            "UPDATE transactions SET category = ? WHERE id = ?",
            (category, txn_id)
        )
        updated += 1

    conn.commit()
    conn.close()
    print(f"Categorized {updated} transactions")

if __name__ == "__main__":
    categorize_all_uncategorized()