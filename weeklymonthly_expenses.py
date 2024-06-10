import tkinter as tk
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from dailyexpenses import DailyExpenseTracker

class WeeklyMonthlyExpenses(DailyExpenseTracker):
    def __init__(self, master):
        self.master = master
        