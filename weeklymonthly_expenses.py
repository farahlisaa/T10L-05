import tkinter as tk
from datetime import datetime, timedelta
from dailyexpenses import DailyExpenseTracker

class WeeklyMonthlyExpenses(DailyExpenseTracker):
    def __init__(self, master):
        self.master = master
        self.master.title("Weekly and Monthly Expenses")

        self.view_weekly_button = tk.Button(master, text="View Weekly Expenses", command=self.view_weekly_expenses)
        self.view_weekly_button.pack()

        self.view_monthly_button = tk.Button(master, text="View Monthly Expenses", command=self.view_monthly_expenses)
        self.view_monthly_button.pack()


        self.expense_summary_frame = tk.Frame(master, bg="#800080")
        self.expense_summary_frame.pack(fill=tk.BOTH, expand=True)

        self.expense_summary_label = tk.Label(self.expense_summary_frame, text="Weekly/Monthly Expenses:", bg="#800080", fg="#FFFFFF")
        self.expense_summary_label.pack()

        self.expense_summary_listbox = tk.Listbox(self.expense_summary_frame, width=50)
        self.expense_summary_listbox.pack()


    def view_weekly_expenses(self):
        expenses_by_category = self.get_expenses_in_period(7)
        self.update_expense_summary_listbox(expenses_by_category)

    def view_monthly_expenses(self):
        expenses_by_category = self.get_expenses_in_period(30)
        self.update_expense_summary_listbox(expenses_by_category)

    def parse_expense_details(self, details):
        category = details.split('(')[-1].split(')')[0].strip()
        expense = float(details.split('RM')[-1].split()[0])
        return category, expense

    def get_expenses_in_period(self, days):
        expenses_by_category = {}
        end_date = datetime.today()
        start_date = end_date - timedelta(days=days)

        for item in self.expense_listbox.get(0, tk.END):
            date_str, details = item.split(': ', 1)
            expense_date = datetime.strptime(date_str, '%d/%m/%Y')
            
            if start_date <= expense_date <= end_date:
                category, expense = self.parse_expense_details(details)
                expenses_by_category[category] = expenses_by_category.get(category, 0) + expense

        return expenses_by_category


    def update_expense_summary_listbox(self, expenses_by_category):
        self.expense_summary_listbox.delete(0, tk.END)
        for category, amount in expenses_by_category.items():
            self.expense_summary_listbox.insert(tk.END, f"{category}: RM{amount:.2f}")


def main():
    root = tk.Tk()
    app = WeeklyMonthlyExpenses(root)
    root.mainloop()

if __name__ == "__main__":
    main()
