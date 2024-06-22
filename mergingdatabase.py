import sqlite3

def merge_expenses_to_user_data():
    try:
        # Connect to expenses.db (source database)
        conn_expenses = sqlite3.connect('expenses.db')
        cursor_expenses = conn_expenses.cursor()

        # Connect to user_data.db (target database)
        conn_user_data = sqlite3.connect('user_data.db')
        cursor_user_data = conn_user_data.cursor()

        # Query to fetch data from expenses.db
        cursor_expenses.execute('SELECT * FROM expenses')

        # Fetch all rows from expenses.db
        rows = cursor_expenses.fetchall()

        # Create a new table in user_data.db based on fetched data structure
        # Assuming expenses table structure: expensesid, userid, date, expense, category
        cursor_user_data.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                expensesid INTEGER PRIMARY KEY,
                userid REAL,
                date TEXT,
                expense REAL,
                category TEXT
            )
        ''')

        # Insert data into user_data.db expenses table
        cursor_user_data.executemany('INSERT INTO expenses VALUES (?, ?, ?, ?, ?)', rows)

        # Commit changes to user_data.db
        conn_user_data.commit()

        print("Data merged successfully.")

    except sqlite3.Error as e:
        print(f"Error merging data: {e}")

    finally:
        # Close connections
        conn_expenses.close()
        conn_user_data.close()

if __name__ == "__main__":
    merge_expenses_to_user_data()
