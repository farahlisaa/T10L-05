import sqlite3
import datetime

connect = sqlite3.connect("expenses.db")
cursor = connect.cursor()

while True:
    print("Select am option:")
    print("1. Enter a new expense")
    print("2. View expenses summary")

    choice = int(input())

    if choice == 1:
        date = input("Enter the date of the expense (YYYY-MM-DD): ")
        description = input("Enter the description of the expense: ")

        cursor.execute("SELECT DISTINCT category FROM expenses")

        categories = cursor.fetchall()

        print("Select a category by number:")
        for idx, category in enumerate(categories):
            print(f"{idx + 1}, {category[0]}")
        print(f"{len(categories) + 1}, Create a new category")

        category_choice = input()
        if category_choice == len(categories) + 1:
            category = input("Enter the new category name: ")
        else:
            category = categories[category_choice - 1][0]

        price = input("Enter the price of the expense: ")

        cursor.execute("INSERT INTO expenses (Date, description, category, price) VALUES (?, ?, ?, ?)")

        connect.commit()

    elif choice == 2:
        print("Select an option:")
        print("1. View all expenses")
        print("2. View monthly expenses by category")
        view_choice = int(input())
        if view_choice == 1:
            cursor.execute("SELECT * FROM expenses")
            expenses = cursor.fetchall()
            for expense in expenses:
                print(expense)
        elif view_choice == 2:
            month = input("Enter the month (MM): ")
            year = input("Enter the year (YYYY): ")
            cursor.execute("SELECT category, SUM(price) FROM expense WHERE strftime('%m', Date) = ? AND strftime('%Y', Date) = ? GROUP BY category", (month, year))
            expenses = cursor.fetchall()
            for expense in expenses:
                print(f"Category: {expense[0]}, Total: {expense[1]}")
    else:
        exit()

connect.close()