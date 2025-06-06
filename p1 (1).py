import csv
import os
from datetime import datetime
from tabulate import tabulate

CSV_FILE = "expenses.csv"

def ensure_file():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Amount", "Category", "Date", "Description"])

def read_expenses():
    ensure_file()
    with open(CSV_FILE, "r") as file:
        return list(csv.DictReader(file))

def write_expenses(expenses):
    with open(CSV_FILE, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["ID", "Amount", "Category", "Date", "Description"])
        writer.writeheader()
        writer.writerows(expenses)

def add_expense():
    ensure_file()
    amount = input("Enter amount: ")
    category = input("Enter category: ")
    date = input("Enter date (YYYY-MM-DD) [leave blank for today]: ") or datetime.today().strftime("%Y-%m-%d")
    description = input("Enter description: ")

    expenses = read_expenses()
    expense_id = str(len(expenses) + 1)

    new_expense = {
        "ID": expense_id,
        "Amount": amount,
        "Category": category,
        "Date": date,
        "Description": description,
    }

    with open(CSV_FILE, "a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=new_expense.keys())
        writer.writerow(new_expense)
    print("Expense added successfully.")

def view_expenses():
    expenses = read_expenses()
    if not expenses:
        print("No expenses found.")
    else:
        print(tabulate(expenses, headers="keys", tablefmt="grid"))

def filter_by_category():
    category = input("Enter category to filter: ")
    expenses = read_expenses()
    filtered = [e for e in expenses if e["Category"].lower() == category.lower()]
    if filtered:
        print(tabulate(filtered, headers="keys", tablefmt="grid"))
    else:
        print("No expenses found in that category.")

def monthly_summary():
    expenses = read_expenses()
    summary = {}
    for e in expenses:
        month = e["Date"][:7]  # YYYY-MM
        cat = e["Category"]
        amount = float(e["Amount"])
        key = (month, cat)
        summary[key] = summary.get(key, 0) + amount

    rows = [{"Month": k[0], "Category": k[1], "Total": v} for k, v in summary.items()]
    print(tabulate(rows, headers="keys", tablefmt="grid"))

def delete_expense():
    expenses = read_expenses()
    if not expenses:
        print("No expenses to delete.")
        return

    view_expenses()
    expense_id = input("Enter ID of the expense to delete: ")
    new_expenses = [e for e in expenses if e["ID"] != expense_id]

    if len(new_expenses) == len(expenses):
        print("Expense ID not found.")
    else:
        write_expenses(new_expenses)
        print("Expense deleted.")

def main():
    while True:
        print("\n=== Personal Expense Tracker ===")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Filter by Category")
        print("4. Monthly Summary")
        print("5. Delete Expense")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            filter_by_category()
        elif choice == "4":
            monthly_summary()
        elif choice == "5":
            delete_expense()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
