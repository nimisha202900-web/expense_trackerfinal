pip install --upgrade pip
import sqlite3
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


# Database setup
conn = sqlite3.connect("expenses.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    category TEXT,
    amount REAL,
    note TEXT
)
""")
conn.commit()

# Streamlit UI
st.title("💰 Simple Expense Tracker")

menu = ["Add Expense", "View Summary", "Visualize Spending"]
choice = st.sidebar.radio("Menu", menu)

if choice == "Add Expense":
    st.subheader("➕ Add a New Expense")
    date = st.date_input("Date", datetime.today())
    category = st.selectbox("Category", ["Food", "Transport", "Rent", "Shopping", "Bills", "Other"])
    amount = st.number_input("Amount", min_value=0.0, step=0.01)
    note = st.text_area("Note (optional)")
    if st.button("Save Expense"):
        cursor.execute(
            "INSERT INTO expenses (date, category, amount, note) VALUES (?, ?, ?, ?)",
            (date.strftime("%Y-%m-%d"), category, amount, note)
        )
        conn.commit()
        st.success("✅ Expense saved successfully!")

elif choice == "View Summary":
    st.subheader("📊 Expense Summary")
    df = pd.read_sql("SELECT * FROM expenses", conn)
    if df.empty:
        st.warning("No expenses recorded yet.")
    else:
        st.dataframe(df)
        df["date"] = pd.to_datetime(df["date"])
        df["month"] = df["date"].dt.to_period("M")
        monthly_total = df.groupby("month")["amount"].sum().reset_index()
        st.write("### Monthly Expenses")
        st.table(monthly_total)
        top_categories = df.groupby("category")["amount"].sum().sort_values(ascending=False).head(3)
        st.write("### Top 3 Spending Categories")
        st.table(top_categories)
        avg_daily = df.groupby("date")["amount"].sum().mean()
        st.write(f"### Average Daily Spend: **₹{avg_daily:.2f}**")

elif choice == "Visualize Spending":
    st.subheader("📈 Spending Visualization")
    df = pd.read_sql("SELECT * FROM expenses", conn)
    if df.empty:
        st.warning("No data to visualize.")
    else:
        category_summary = df.groupby("category")["amount"].sum().reset_index()
        fig, ax = plt.subplots()
        ax.bar(category_summary["category"], category_summary["amount"], color="teal")
        ax.set_xlabel("Category")
        ax.set_ylabel("Total Spent")
        ax.set_title("Spending by Category")
        st.pyplot(fig)

> Replace `nimisha202900-web` with your GitHub username.

---

### **Step 5: Push to GitHub**

```bash
git init
git add .
git commit -m "Initial commit: Expense Tracker Streamlit App"
git branch -M main
git remote add origin https://github.com/<your-username>/expense-tracker.git
git push -u origin main
