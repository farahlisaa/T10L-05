import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime


class SavingTracker:
    def __init__(self, root):
        self.root = root

        self.budget_data = {}

        #window setting
        self.root.title('Saving Tracker')
        self.root.state('zoomed')
        self.root.configure(bg = 'white')
        self.root.resizable(False, False)

        self.frame = tk.Frame(self.root, bg = 'white')
        self.frame.place(x = 800, y = 150)

        self.heading = tk.Label(self.root, text = 'Saving Tracker', font = ('Helvetica', 23, 'bold'), bg = 'white', fg = 'black')
        self.heading.grid(row = 0, column = 0, padx = 200, pady = 50)

        #date feature
        self.date_label = ttk.Label(self.frame, text = "Date (DD/MM/YYYY):", background = 'white')
        self.date_label.grid(row = 0, column = 0, padx = 5, pady = 5)
        self.date_entry = ttk.Entry(self.frame)
        self.date_entry.grid(row = 0, column = 1, padx = 5, pady = 5)

        #amount feature
        self.amount_label = ttk.Label(self.frame, text = "Amount:", background = 'white')
        self.amount_label.grid(row = 1, column = 0, padx = 5, pady = 5)
        self.amount_entry = ttk.Entry(self.frame)
        self.amount_entry.grid(row = 2, column = 1, padx = 5, pady = 5)

        #category feature
        self.category_label = ttk.Label(self.frame, text="Category:", background='white')
        self.category_label.grid(row=2, column=0, padx=5, pady=5)
        self.category_combobox = ttk.Combobox(self.frame, values=["Food", "Bills", "Shopping", "Others"])
        self.category_combobox.grid(row=2, column=1, padx=5, pady=5)
        self.category_combobox.set("Food")

        #add button
        self.add_button = ttk.Button(self.frame, text = "Add", command = self.add_saving)
        self.add_button.grid(row = 3, column = 0, columnspan = 2, pady = 5)

        #plot feature
        self.figure = plt.Figure(figsize = (8, 6), dpi = 100)
        self.ax = self.figure.add_subplot(111)
        self.chart_type = FigureCanvasTkAgg(self.figure, self.root)
        self.chart_type.get_tk_widget().place(x = 800, y = 350)

    def add_saving(self):
        date_str = self.date_entry.get()
        amount_str = self.amount_entry.get()
        category = self.category_combobox.get()

        try:
            date = datetime.datetime.strptime(date_str, date_pattern = 'DD/MM/YYYY')
            amount = float(amount_str)

            month = date.strftime("%Y-%m")
            if month not in self.budget_data:
                self.budget_data[month] = {"Food": 0, "Bills": 0, "Shopping": 0, "Others": 0}
            self.budget_data[month][category] += amount

            self.date_entry.delete(0, tk.END)
            self.amount_entry.delete(0, tk.END)

            self.update_chart()
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter a valid date and amount.")

    def update_chart(self):
        self.ax.clear()

        months = sorted(self.budget_data.keys())
        categories = [ "Food", "Bills", "Shopping", "Others"]
        category_totals = {category: [] for category in categories}

        for month in months:
            for category in categories:
                category_totals[category].append(self.budget_data[month][category])

        bar_width = 0.2
        for idx, category in enumerate(categories):
            self.ax.bar(
                [i +idx *bar_width for i in range(len(months))],
                category_totals[category],
                bar_width,
                label = category
            )

        self.ax.set_title('Monthly Saving Tracker')
        self.ax.set_xlabel('Month')
        self.ax.set_ylabel('Total Amount')
        self.ax.set_xticks([i +bar_width for i in range(len(months))])
        self.ax.set_xticklabels(months)
        self.ax.legend()

        self.chart_type.draw()

if __name__ == "__main__":
    saving_window = tk.Tk()
    app = SavingTracker(saving_window)
    saving_window.mainloop()