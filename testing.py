import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
from datetime import datetime
import matplotlib.pyplot as plt
import sqlite3
from notification import NotificationHandler

class DailyExpenseTracker:
    def __init__(self, master):
        self.master = master
        self.master.title("Daily Expenses Tracker")
        self.master.config(bg="#800080")

        self.connect = sqlite3.connect('expenses.db')
        self.c = self.connect.cursor()
        self.update_table_schema()

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

        # Create notification handler instance
        self.notification_handler = NotificationHandler(self)

        self.initialize()

    def initialize(self):
        self.weekly_expenses_button = tk.Button(self.master, text="Calculate Weekly Expenses", command=self.calculate_weekly_expenses)
        self.weekly_expenses_button.pack()

        self.weekly_total_label = tk.Label(self.master, text="Weekly Expenses by Category:", bg="#800080", fg="#FFFFFF")
        self.weekly_total_label.pack()

        self.weekly_expenses_text = tk.Text(self.master, height=10, width=50)
        self.weekly_expenses_text.pack()

        self.monthly_expenses_button = tk.Button(self.master, text="Calculate Monthly Expenses", command=self.calculate_monthly_expenses)
        self.monthly_expenses_button.pack()

        self.monthly_total_label = tk.Label(self.master, text="Monthly Expenses by Category:", bg="#800080", fg="#FFFFFF")
        self.monthly_total_label.pack()

        self.monthly_expenses_text = tk.Text(self.master, height=10, width=50)
        self.monthly_expenses_text.pack()

    def update_table_schema(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS expenses
                          (expensesid INTEGER PRIMARY KEY,
                          userid REAL,
                          date TEXT,
                          expense REAL,
                          category TEXT)''')
        self.connect.commit()

    def select_date(self):
        top = tk.Toplevel(self.master)
        cal = Calendar(top, selectmode="day", date_pattern='dd/MM/yyyy')
        cal.pack()
        def set_date():
            self.date_var.set(cal.get_date())
            top.destroy()
        select_button = tk.Button(top, text="Select", command=set_date)
        select_button.pack()

    def insert_expense(self, expense_date, expense, expense_category):
        userid = 1
        self.c.execute("INSERT INTO expenses (userid, date, expense, category) VALUES (?, ?, ?, ?)",
                       (userid, expense_date, expense, expense_category))
        self.connect.commit()

    def add_expense(self):
        try:
            expense = float(self.expense_entry.get())
            self.total_expenses += expense
            self.total_label.config(text="Total Expenses: RM {:.2f}".format(self.total_expenses))
            self.expense_entry.delete(0, tk.END)
            expense_date = self.date_var.get()
            expense_category = self.category_var.get()
            self.expense_listbox.insert(tk.END, f"{expense_date}: RM{expense:.2f} ({expense_category})")
            self.insert_expense(expense_date, expense, expense_category)

            # After adding expense, recalculate weekly expenses
            self.calculate_weekly_expenses()
            self.calculate_monthly_expenses()

            # Check if notifications should be shown
            self.notification_handler.show_notification_if_no_expenses()

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

    def calculate_weekly_expenses(self):
        today = datetime.today()
        start_of_week = today - timedelta(days=today.weekday())  # Start of the week is Monday
        end_of_week = start_of_week + timedelta(days=6)  # End of the week is Sunday

        self.c.execute("""
            SELECT category, SUM(expense) 
            FROM expenses 
            WHERE date BETWEEN ? AND ? 
            GROUP BY category
        """, (start_of_week.strftime('%d/%m/%Y'), end_of_week.strftime('%d/%m/%Y')))
        weekly_expenses = self.c.fetchall()

        total_weekly_expenses = sum(total for _, total in weekly_expenses)

        self.weekly_expenses_text.delete(1.0, tk.END)
        if weekly_expenses:
            for category, total in weekly_expenses:
                self.weekly_expenses_text.insert(tk.END, f"{category}: RM{total:.2f}\n")
            self.weekly_expenses_text.insert(tk.END, f"\nTotal Weekly Expenses: RM{total_weekly_expenses:.2f}")
        else:
            self.weekly_expenses_text.insert(tk.END, "No expenses recorded for this week.")

    def calculate_monthly_expenses(self):
        # Get user input date
        input_date_str = self.date_var.get()
        input_date = datetime.strptime(input_date_str, '%d/%m/%Y')

        # Determine start and end of the month based on the input date
        start_of_month = input_date.replace(day=1)
        end_of_month = start_of_month.replace(day=calendar.monthrange(start_of_month.year, start_of_month.month)[1])

        # Query for expenses only if they fall within the same month as the input date
        self.c.execute("""
            SELECT category, SUM(expense) 
            FROM expenses 
            WHERE date BETWEEN ? AND ?
            GROUP BY category
        """, (start_of_month.strftime('%d/%m/%Y'), end_of_month.strftime('%d/%m/%Y')))
        monthly_expenses = self.c.fetchall()

        total_monthly_expenses = sum(total for _, total in monthly_expenses)

        self.monthly_expenses_text.delete(1.0, tk.END)
        if monthly_expenses:
            for category, total in monthly_expenses:
                self.monthly_expenses_text.insert(tk.END, f"{category}: RM{total:.2f}\n")
            self.monthly_expenses_text.insert(tk.END, f"\nTotal Monthly Expenses: RM{total_monthly_expenses:.2f}")
        else:
            self.monthly_expenses_text.insert(tk.END, "No expenses recorded for this month.")

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




