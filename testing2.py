import tkinter as tk
from tkinter import messagebox

class Expense:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def get_name(self):
        return self.name
    
    def get_value(self):
        return self.value
    
class ExpenseCalculator:
    def __init__(self, root_value):
        self.weekly_earnings_label = None
        self.monthly_earnings_label = None
        self.salary_input = None
        self.remaining_income_label = None
        self.result_label = None
        self.calculation_choice_spinner = None
        self.calculation_choice = None
        self.expenses_list = None
        self.custom_expense_value = None
        self.custom_expense_name = None
        self.root = root_value
        self.root.title("HExpense Calculator")
        self.root.configure(bg="#F0F0F0")

        self.expenses = []

        self.setup_expenses_frame()

        self.setup_delete_expenses_frame()

        self.setup_calculation_choice_frame()

        self.setup_calculate_expenses_button()

        self.setup_result_label()

        self.setup_monthly_earnings_frame()

        self.setup_calculate_earnings_button()

        self.setup_earnings_labels()

        self.setup_remaining_income_label()

    def setup_expenses_frame(self):
        #allows users to input custom expenses and display the list of expenses

        expenses_frame = tk.LabelFrame(
            self.root, text="Expenses", font=("Arial", 14, "bold"), bg="#F0F0F0"
        )
        expenses_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")