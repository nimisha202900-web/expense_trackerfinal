# ===============================
# 1. Setup
# ===============================
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np

# Create DB
conn = sqlite3.connect("expenses.db")
cur = conn.cursor()

# Create Table
cur.execute("""
CREATE TABLE IF NOT EXISTS Expenses (
    expense_id INTEGER PRIMARY KEY,
    date TEXT,
    category TEXT,
    amount REAL,
    note TEXT
)
""")
conn.commit()

# ===============================
# 2. Calculator-like Input
# ===============================
def add_expense():
    print("\n💰 Add New Expense Entry")
    date = input("Enter date (YYYY-MM-DD) or press Enter for today: ")
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")

    category = input("Enter category (Food, Rent, Travel, Shopping, Other): ")
    amount = float(input("Enter amount: ₹ "))
    note = input("Enter note (optional): ")

    cur.execute("INSERT INTO Expenses (date, category, amount, note) VALUES (?, ?, ?, ?)",
                (date, category, amount, note))
    conn.commit()
    print("✅ Expense added successfully!\n")

# Add expenses interactively
while True:
    choice = input("Do you want to add an expense? (y/n): ").lower()
    if choice == "y":
        add_expense()
    else:
        break

# ===============================
# 3. Queries
# ===============================

# Total Monthly Expenses
query_monthly = """
SELECT strftime('%Y-%m', date) AS month, SUM(amount) as total
FROM Expenses
WHERE date IS NOT NULL -- Add this condition to filter out NULL dates
GROUP BY month
ORDER BY month
"""
monthly_expenses = pd.read_sql(query_monthly, conn)
print("\n📊 Total Monthly Expenses:\n", monthly_expenses)

# Top 3 Categories
query_top3 = """
SELECT category, SUM(amount) as total
FROM Expenses
GROUP BY category
ORDER BY total DESC
LIMIT 3
"""
top3_categories = pd.read_sql(query_top3, conn)
print("\n🔥 Top 3 Spending Categories:\n", top3_categories)

# Average Daily Spend
query_avg = """
SELECT AVG(daily_total) as avg_daily_spend
FROM (
    SELECT date, SUM(amount) as daily_total
    FROM Expenses
    GROUP BY date
)
"""
avg_daily = pd.read_sql(query_avg, conn)
print("\n💵 Average Daily Spend:\n", avg_daily)

# ===============================
# 4. Visualization (Fixed)
# ===============================
if not monthly_expenses.empty:
    # Ensure "month" is string (for x-axis labels)
    monthly_expenses["month"] = monthly_expenses["month"].astype(str)

    plt.figure(figsize=(8,5))
    plt.bar(monthly_expenses["month"], monthly_expenses["total"], color="teal")
    plt.title("Monthly Expense Trend")
    plt.xlabel("Month")
    plt.ylabel("Total Expenses (₹)")
    plt.xticks(rotation=45)
    plt.show()
else:
    print("\n(No expenses recorded yet for visualization.)")




---

### **Step 5: Push to GitHub**

```bash
git init
git add .
git commit -m "Initial commit: Expense Tracker Streamlit App"
git branch -M main
git remote add origin https://github.com/<your-username>/expense-tracker.git
git push -u origin main
