import datetime
import json
import os
from typing import List, Dict

DATA_FILE = "finance_data.json"

def load_data() -> Dict:
    if not os.path.exists(DATA_FILE):
        return {"income": [], "expenses": []}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data: Dict):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def add_income(source: str, amount: float, date: str):
    data = load_data()
    entry = {"source": source, "amount": amount, "date": date}
    data["income"].append(entry)
    save_data(data)

def add_expense(category: str, amount: float, date: str):
    data = load_data()
    entry = {"category": category, "amount": amount, "date": date}
    data["expenses"].append(entry)
    save_data(data)

def list_incomes():
    data = load_data()
    return data["income"]

def list_expenses():
    data = load_data()
    return data["expenses"]

def get_balance():
    data = load_data()
    income_total = sum(entry["amount"] for entry in data["income"])
    expense_total = sum(entry["amount"] for entry in data["expenses"])
    return income_total - expense_total

def get_summary_by_category() -> Dict[str, float]:
    data = load_data()
    summary = {}
    for expense in data["expenses"]:
        cat = expense["category"]
        summary[cat] = summary.get(cat, 0) + expense["amount"]
    return summary

def filter_expenses_by_date(start: str, end: str) -> List[Dict]:
    start_date = datetime.datetime.strptime(start, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end, "%Y-%m-%d")
    data = load_data()
    return [e for e in data["expenses"] if start_date <= datetime.datetime.strptime(e["date"], "%Y-%m-%d") <= end_date]

def pretty_print(data: List[Dict], title: str):
    print(f"\n--- {title} ---")
    for entry in data:
        print(entry)

def print_summary():
    print("\n==== Finance Summary ====")
    print(f"Balance: ₹{get_balance():,.2f}")
    print("\nExpenses by Category:")
    summary = get_summary_by_category()
    for category, amount in summary.items():
        print(f"  {category}: ₹{amount:,.2f}")

def main_menu():
    while True:
        print("""
1. Add Income
2. Add Expense
3. View Incomes
4. View Expenses
5. View Balance
6. Summary by Category
7. Filter Expenses by Date
8. Exit
        """)
        choice = input("Select an option: ")

        if choice == '1':
            src = input("Enter source: ")
            amt = float(input("Enter amount: "))
            dt = input("Enter date (YYYY-MM-DD): ")
            add_income(src, amt, dt)
        elif choice == '2':
            cat = input("Enter category: ")
            amt = float(input("Enter amount: "))
            dt = input("Enter date (YYYY-MM-DD): ")
            add_expense(cat, amt, dt)
        elif choice == '3':
            pretty_print(list_incomes(), "All Incomes")
        elif choice == '4':
            pretty_print(list_expenses(), "All Expenses")
        elif choice == '5':
            print(f"\nCurrent Balance: ₹{get_balance():,.2f}")
        elif choice == '6':
            print_summary()
        elif choice == '7':
            start = input("Enter start date (YYYY-MM-DD): ")
            end = input("Enter end date (YYYY-MM-DD): ")
            filtered = filter_expenses_by_date(start, end)
            pretty_print(filtered, f"Expenses from {start} to {end}")
        elif choice == '8':
            print("Exiting... Bye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main_menu()
