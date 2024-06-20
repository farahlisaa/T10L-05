from tkinter import *
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
import os

class MonthlySavingsTracker:
    #window setting
    def __init__(self, root):
        self.root = root
        self.root.title("Monthly Savings Tracker")
        self.root.state('zoomed')
        self.root.configure(bg = 'white')
        self.root.resizable(False, False)

    #categories options
        self.categories = ["Food", "Shopping", "Bills", "Entertainment", "Others"]
        self.savings = {}

        self.load_data()

        self.input_frame = Frame(self.root, bg = 'white')
        self.input_frame.pack(pady = 20)

    #amount label
        self.amount_label = Label(self.input_frame, text = "Enter Savings Amount (RM):", bg = 'white', font = ('Helvetica', 15))
        self.amount_label.grid(row = 0, column = 0, padx = 10, pady = 10)
    #amount entry
        self.amount_entry = Entry(self.input_frame)
        self.amount_entry.grid(row = 0, column = 1, padx = 10, pady = 10)
    #category label
        self.category_label = Label(self.input_frame, text = "Select Category:", bg = 'white', font = ('Helvetica', 15))
        self.category_label.grid(row = 1, column =0, padx = 10, pady = 10)
    #category menu
        self.category_var = StringVar(self.input_frame)
        self.category_var.set(self.categories[0])
        self.categories_menu = OptionMenu(self.input_frame, self.category_var, *self.categories)
        self.categories_menu.grid(row = 1,column = 1, padx = 10, pady = 10)

    #month label
        self.month_label = Label(self.input_frame, text = "Select Month:", bg = 'white', font = ('Helvetica', 15))
        self.amount_label.grid(row = 2, column = 0, padx = 10, pady = 10)
    #month menu
        self.month_var = StringVar(self.input_frame)
        self.month_var.set("January")
        self.month_menu = OptionMenu(self.input_frame, self.month_var, *self.month_options())
        self.month_menu.grid(row = 2, column = 1, padx = 10, pady = 10)

    #add button
        self.add_button = Button(self.input_frame, text = "Add Savings", font = ('Helvetica', 10), command = self.add_savings)
        self.add_button.grid(row = 0, column = 2, rowspan = 3, padx = 10, pady = 10)
    #chart button
        self.show_chart_button = Button(self.input_frame, text = "Show Chart", font = ('Helvetica', 10), command = self.show_chart)
        self.show_chart_button.grid(row = 3, columnspan = 3, pady = 10)

        self.chart_frame = Frame(self.root, bg = 'white')
        self.chart_frame.pack()

    #month options command
    def month_options(self):
        return["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    
    #add savings command
    def add_savings(self):
        amount = self.amount_entry.get()
        category = self.category_var.get()
        month = self.month_var.get()

        if amount:
            try:
                amount = float(amount)
                if month not in self.savings:
                    self.savings[month] = {category: 0 for category in self.categories}
                self.savings[month][category] += amount
                messagebox.showinfo("Success", "Savings added successfully!")
                self.amount_entry.delete(0, END)
                self.save_data()
                self.show_chart()
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number")
        else:
            messagebox.showerror("Error", "Please enter an amount")

    #show chart command
    def show_chart(self):
        for widget in self.chart_frame.winfo_children():
            widget.destroy

        current_month = self.month_var.get()
        previous_month = self.get_previous_month(current_month)

        #chart setup
        fig, ax = plt.subplots()

        categories = self.categories
        current_amounts = [self.savings.get(current_month, {}).get(category, 0) for category in categories]
        previous_amounts = [self.savings.get(previous_month, {}).get(category, 0) for category in categories]

        bar_width = 0.3
        index = range(len(categories))

        ax.bar(index, current_amounts, bar_width, label = current_month)
        ax.bar([i + bar_width for i in index], previous_amounts, bar_width, label = previous_month)

        ax.set_xlabel("Categories")
        ax.set_ylabel("Amount")
        ax.set_title("Total Saving by Category")
        ax.set_xticks([i + bar_width / 2 for i in index])
        ax.set_xticklabels(categories)
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master = self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    #get previous month
    def get_previous_month(self, current_month):
        month_list = self.month_options()
        current_index = month_list.index(current_month)
        previous_index = (current_index - 1) % len(month_list)
        return month_list[previous_index]
    
    #save data
    def save_data(self):
        with open('savings_data.json', 'w') as file:
            json.dump(self.savings, file)
    #load data
    def load_data(self):
        if os.path.exists('savings_data.json'):
            with open('savings_data.json', 'r') as file:
                self.savings = json.load(file)

#window looping
if __name__ == '__main__':
    root = Tk()
    app = MonthlySavingsTracker(root)
    root.mainloop()