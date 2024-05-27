import sqlite3

connect = sqlite3.connect("expenses.db")
cursor = connect.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS expenses (id INTEGER PRIMARY KEY, Date DATE, description TEXT, category TEXT, price REAL)")

connect.commit()
connect.close()