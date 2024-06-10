from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime


#window setting
saving_window = Tk()
saving_window.title('Sign Up Page')
saving_window.state('zoomed')
saving_window.configure(bg = 'white')
saving_window.resizable(False, False)

frame = Frame(saving_window, bg = 'white')
frame.place(x = 800, y = 100)

heading = Label(saving_window, text = 'CREATE AN ACCOUNT', font = ('Helvetica', 23, 'bold'), bg = 'white', fg = 'black')
heading.grid(row = 0, column = 0, padx = 200, pady = 50)



saving_window.mainloop()

class SavingsTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Savings Tracker")

        self.savings_data = []

        self.date_label = ttk.Label(root, text = "Date (YYYY-MM-DD):")
        self.date_label.grid(row = 0, column = 0, padx = 5, pady = 5)
        self.date_entry = ttk.Entry(root)
        self.date_entry.grid(row = 0, column = 1, padx = 5, pady = 5)

        self.amount_label = ttk.Label(root, text = "Amount Saved:")
        self.amount_label.grid(row = 1, column = 0, padx = 5, pady = 5)
        self.amount_entry = ttk.Entry(root)
        self.amount_entry.grid(row = 1, column = 0, padx = 5, pady = 5)

        self.add_button = ttk.Button(root, text = "Add", command = self.add_saving)
        self.add_button.grid(row = 2, column = 0, padx = 5, pady = 5)

        self.figure = plt.Figure(figsize = (6, 4), dpi = 100)
        self.ax = self.figure.add_subplot(111)
        self.chart_type = FigureCanvasTkAgg(self.figure, root)
        self.chart_type.get_tk_widget().grid(row = 3, column = 0, columnspan = 2)


    def add_saving(self):
        date_str = self.date_entry.get()
        amount_str = self.amount_entry.get()

        try:
            date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            amount = float(amount_str)

            self.savings_data.append((date, amount))
            self.date_entry.delete(0, tk.END)
            self.amount_entry.delete(0, tk.END)

            self.update_chart()
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter a valid date and amount.")

    
    def update_chart(self):
        dates = [entry[0] for entry in self.savings_data]
        amounts = [entry[1] for entry in self.savings_data]

        self.ax.clear()
        self.ax.bar(dates, amounts)
        self.ax.set_title('Savings Over Time')
        self.ax.set_xlabel('Date')
        self.ax.set_ylabel('Amount Saved')
        self.figure.autofmt_xdate()

        self.chart_type.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = SavingsTracker(root)
    root.mainloop()