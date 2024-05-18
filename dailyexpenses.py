import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
from tkinter import ttk
from datetime import datetime

class DailyExpenseTracker:
    def __init__(self, master):
        self.master = master
        self.master.title("Daily Expense Tracker")

        self.date_label = tk.Label(master, text="Date:")
        self.date_label.pack()

        self.date_var = tk.StringVar(master, value=datetime.today().strftime('%d/%m/%Y'))
        self.date_entry = tk.Entry(master, textvariable=self.date_var)
        self.date_entry.pack()

        self.date_button = tk.Button(master, text="Choose Date", command=self.select_date)
        self.date_button.pack()

        self.categories = ["Food", "Transportation", "Utilities", "Groceries", "Other"]

        self.expense_label = tk.Label(master, text="Enter Expense (RM):")
        self.expense_label.pack()

        self.expense_entry = tk.Entry(master)
        self.expense_entry.pack()

        self.category_label = tk.Label(master, text="Select Category:")
        self.category_label.pack()

        self.category_var = tk.StringVar(master)
        self.category_var.set(self.categories[0])

        self.category_menu = tk.OptionMenu(master, self.category_var, *self.categories)
        self.category_menu.pack()

        self.add_expense_button = tk.Button(master, text="Add Expense", command=self.add_expense)
        self.add_expense_button.pack()

        self.expense_list_label = tk.Label(master, text="Expenses:")
        self.expense_list_label.pack()

        self.expense_listbox = tk.Listbox(master, width=50)
        self.expense_listbox.pack()

        self.total_label = tk.Label(master, text="Total Expenses: RM0.00")
        self.total_label.pack()

        self.total_expenses = 0.0

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
