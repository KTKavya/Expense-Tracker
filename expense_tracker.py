import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load or initialize CSV
def load_data():
    try:
        return pd.read_csv("expense_history.csv", parse_dates=["Date"])
    except FileNotFoundError:
        return pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])

def save_data(df):
    df.to_csv("expense_history.csv", index=False)

# 1. Add Expense
def add_expense(df):
    date = input("Enter date (YYYY-MM-DD): ")
    category = input("Enter category : ")
    try:
        amount = float(input("Enter amount: "))
    except ValueError:
        print("Invalid amount.")
        return df
    desc = input("Enter description: ")
    new_entry = pd.DataFrame([[pd.to_datetime(date), category, amount, desc]],
                             columns=df.columns)
    df = pd.concat([df, new_entry], ignore_index=True)
    save_data(df)
    print(" Expense added successfully.\n")
    return df

# 2. Total Spending Overview
def total_overview(df):
    if df.empty:
        print("No data to analyze.\n")
        return
    total = df['Amount'].sum()
    max_expense = df.loc[df['Amount'].idxmax()]
    min_expense = df.loc[df['Amount'].idxmin()]
    print(f"\n Total Spent: ₹{total:.2f}")
    print("\n Highest Expense:")
    print(max_expense)
    print("\n Lowest Expense:")
    print(min_expense)

# 3. Category-wise Analysis
def category_analysis(df):
    if df.empty:
        print("No data to analyze.\n")
        return
    group = df.groupby("Category")["Amount"]
    total = group.sum()
    count = group.count()
    percent = (total / total.sum() * 100).round(2)
    summary = pd.DataFrame({
        "Total Spent": total,
        "Transactions": count,
        "Percentage (%)": percent
    })
    print("\n Category-wise Summary:")
    print(summary)

    show_pie = input("Do you want to see a pie chart? (y/n): ").lower()
    if show_pie == "y":
        total.plot.pie(autopct='%1.1f%%', startangle=140)
        plt.title("Expenses by Category")
        plt.ylabel("")
        plt.tight_layout()
        plt.show()

# 4. Filter by Date
def filter_by_date(df):
    try:
        start = pd.to_datetime(input("Enter start date (YYYY-MM-DD): "))
        end = pd.to_datetime(input("Enter end date (YYYY-MM-DD): "))
    except ValueError:
        print(" Invalid date format.")
        return
    filtered = df[(df["Date"] >= start) & (df["Date"] <= end)]
    print(f"\nFiltered records from {start.date()} to {end.date()}:\n")
    print(filtered)
    if not filtered.empty:
        summary = filtered.groupby("Category")["Amount"].sum()
        print("\nCategory-wise Totals in Date Range:\n", summary)

# 5. Export Report
def export_summary(df):
    if df.empty:
        print("No data to export.")
        return
    group = df.groupby("Category")["Amount"]
    summary = pd.DataFrame({
        "Total Spent": group.sum(),
        "Transactions": group.count(),
        "Percentage (%)": (group.sum() / group.sum().sum() * 100).round(2)
    })
    summary.to_csv("summary_report.csv")
    print(" Exported summary_report.csv successfully.")

# Menu
def menu():
    df = load_data()
    while True:
        print("\n Expense Tracker Menu")
        print("1. Add Expense")
        print("2. Total Spending Overview")
        print("3. Category-wise Analysis")
        print("4. Filter Expenses by Date Range")
        print("5. Export Summary Report")
        print("6. Exit")
        choice = input("Choose an option (1-6): ")

        if choice == "1":
            df = add_expense(df)
        elif choice == "2":
            total_overview(df)
        elif choice == "3":
            category_analysis(df)
        elif choice == "4":
            filter_by_date(df)
        elif choice == "5":
            export_summary(df)
        elif choice == "6":
            print(" Exiting... OK,Thank You !")
            break
        else:
            print(" Invalid choice. Try again.")

if __name__ == "__main__":
    menu()
