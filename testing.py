import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
from datetime import datetime
import matplotlib.pyplot as plt
import sqlite3

conn = sqlite3.connect('expenses.db')
cursor = conn.cursor()

cursor.execute('SELECT * FROM expenses')

rows = cursor.fetchall()
for row in rows:
    print(row)

conn.close()
class DailyExpenseTracker:
    def __init__(self, master):
        self.master = master
        self.master.title("Daily Expenses Tracker")
        self.master.config(bg="#800080")

        self.connect = sqlite3.connect('expenses.db')
        self.c = self.connect.cursor()
        self.create_table()

        self.date_label = tk.Label(master, text="Date:", bg="#800080", fg="#FFFFFF")
        self.date_label.pack()

        self.date_var = tk.StringVar(master, value=datetime.today().strftime('%d/%m/%Y'))
        self.date_entry = tk.Entry(master, textvariable=self.date_var)
        self.date_entry.pack()

        self.date_button = tk.Button(master, text="Choose Date", command=self.select_date)
        self.date_button.pack()

        self.categories = ["Food", "Transportation", "Utilities", "Groceries", "Other"]

        self.expense_label = tk.Label(master, text="Enter Expense (RM):", bg="#800080", fg="#FFFFFF")
        self.expense_label.pack()

        self.expense_entry = tk.Entry(master)
        self.expense_entry.pack()

        self.category_label = tk.Label(master, text="Select Category:", bg="#800080", fg="#FFFFFF")
        self.category_label.pack()

        self.category_var = tk.StringVar(master)
        self.category_var.set(self.categories[0])

        self.category_menu = tk.OptionMenu(master, self.category_var, *self.categories)
        self.category_menu.config(bg="#FFC0CB")
        self.category_menu.pack()

        self.add_expense_button = tk.Button(master, text="Add Expense", command=self.add_expense)
        self.add_expense_button.pack()

        self.view_mode = "list"

        self.toggle_view_button = tk.Button(master, text="View as Pie Chart", command=self.toggle_view)
        self.toggle_view_button.pack()

        self.expense_list_label = tk.Label(master, text="Expenses:", bg="#800080", fg="#FFFFFF")
        self.expense_list_label.pack()

        self.expense_listbox = tk.Listbox(master, width=50)
        self.expense_listbox.pack()

        self.total_label = tk.Label(master, text="Total Expenses: RM0.00", bg="#800080", fg="#FFFFFF")
        self.total_label.pack()

        self.total_expenses = 0.0

    def create_table(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS expenses
                        (id INTEGER PRIMARY KEY,
                         date TEXT,
                         expense REAL,
                         category TEXT)''')
        self.connect.commit()

    def select_date(self):
        top = tk.Toplevel(self.master)
        cal = Calendar(top, selectmode="day", date_pattern='DD/MM/YYYY')
        cal.pack()
        def set_date():
            self.date_var.set(cal.get_date())
            top.destroy()
        select_button = tk.Button(top, text="Select", command=set_date)
        select_button.pack()

    def add_expense(self):
        try:
            expense = float(self.expense_entry.get())
            self.total_expenses += expense
            self.total_label.config(text="Total Expenses: RM {:.2f}".format(self.total_expenses))
            self.expense_entry.delete(0, tk.END)
            expense_date = self.date_var.get()
            expense_category = self.category_var.get()
            self.expense_listbox.insert(tk.END, f"{expense_date}: RM{expense} ({expense_category})")

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid expense amount.")

    def toggle_view(self):
        if self.view_mode == "list":
            self.view_mode = "pie"
            self.toggle_view_button.config(text="View as List")
            self.update_pie_chart()
        elif self.view_mode == "pie":
            self.view_mode = "list"
            self.toggle_view_button.config(text="View as Pie Chart")
            plt.close()

    def update_pie_chart(self):
        expenses_by_category = {}
        for item in self.expense_listbox.get(0, tk.END):
            category = item.split('(')[-1].split(')')[0].strip()
            expense = float(item.split('RM')[-1].split()[0])
            if category in expenses_by_category:
                expenses_by_category[category] += expense
            else:
                expenses_by_category[category] = expense

        categories = list(expenses_by_category.keys())
        expenses = list(expenses_by_category.values())

        plt.figure(figsize=(5,4))
        plt.pie(expenses, labels=categories, autopct='%1.1f%%')
        plt.title('Expenses by Category')
        plt.axis('equal')
        plt.show()

    def delete_expense(self):
        selected_index = self.expense_listbox.curselection()
        if selected_index:
            self.expense_listbox.delete(selected_index)


def main():
    root = tk.Tk()
    app = DailyExpenseTracker(root)
    root.mainloop()

if __name__ == "__main__":
    main()