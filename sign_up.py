from tkinter import *
from tkinter import messagebox
import sqlite3
import re

def login_page():
    signup_window.destroy()
    import sign_in

#database
def create_database():
    connect = sqlite3.connect('user_data.db')
    c = connect.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT UNIQUE NOT NULL, username TEXT UNIQUE NOT NULL, password TEXT NOT NULL
    )
            ''')

    connect.commit()
    connect.close()

create_database()

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def sign_up():
    username = usernameEntry.get()
    email = emailEntry.get()
    password = passwordEntry.get()
    confirm_password = confirm_passwordEntry.get()

    if password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match.")
        return
    
    if not is_valid_email(email):
        messagebox.showerror("Error", "Invalid email address.")
        return

    try:
        connect = sqlite3.connect('user_data.db')
        c = connect.cursor()

        c.execute('INSERT INTO users (email, username, password) VALUES (?, ?, ?)', 
                  (email, username, password))
        
        connect.commit()
        connect.close()

        messagebox.showinfo("Success", "User signed up successfully!")

        login_page()

    except sqlite3.IntegrityError as e:
        if 'UNIQUE constraint failed' in str(e):
            messagebox.showerror("Error", "Username or email already exists. Please choose a different username or email.")
        else:
            messagebox.showerror("Error", "An error occurred: " + str(e))
    
        

#window setting
signup_window = Tk()
signup_window.title('Sign Up Page')
signup_window.state('zoomed')
signup_window.configure(bg = '#FCC0CB')

frame = Frame(signup_window, bg = 'white')
frame.grid(padx = 20, pady = 20)

heading = Label(frame, text = 'CREATE AN ACCOUNT', font = ('Helvetica', 23, 'bold'), bg = 'white', fg = 'black')
heading.grid(row = 0, column = 0, padx = 10, pady = 10)

#logo
logo = PhotoImage(file = 'logo.png')
app_logo = Label(signup_window, image = logo, bd = 3, bg =  'white')
app_logo.place(x = 500, y = 25)

#email label
emailLabel = Label(frame, text = 'Email:', font = ('Helvetica', 17), bg = 'white', fg = 'black')
emailLabel.grid(row = 7, column = 0, sticky = 'w', padx = 25, pady = (10, 0))
emailEntry = Entry(frame, width = 25, font = ('Helvetica', 17), bg = '#800080', fg = 'white')
emailEntry.grid(row = 8, column = 0, sticky = 'w', padx = 29)

#username label
usernameLabel = Label(frame, text = 'Username:', font = ('Helvetica', 17), bg = 'white', fg = 'black')
usernameLabel.grid(row = 9, column = 0, sticky = 'w', padx = 25, pady = (10, 0))
usernameEntry = Entry(frame, width = 25, font = ('Helvetica', 17), bg = '#800080', fg = 'white')
usernameEntry.grid(row = 10, column = 0, sticky = 'w', padx = 29)

#password label
passwordLabel = Label(frame, text = 'Password:', font = ('Helvetica', 17), bg = 'white', fg = 'black')
passwordLabel.grid(row = 11, column = 0, sticky = 'w', padx = 25, pady = (10, 0))
passwordEntry = Entry(frame, width = 25, font = ('Helvetica', 17), bg = '#800080', fg = 'white')
passwordEntry.grid(row = 12, column = 0, sticky = 'w', padx = 29)

#confirm password label
confirm_passwordLabel = Label(frame, text = 'Confirm Password:', font = ('Helvetica', 17), bg = 'white', fg = 'black')
confirm_passwordLabel.grid(row = 13, column = 0, sticky = 'w', padx = 25, pady = (10, 0))
confirm_passwordEntry = Entry(frame, width = 25, font = ('Helvetica', 17), bg = '#800080', fg = 'white')
confirm_passwordEntry.grid(row = 14, column = 0, sticky = 'w', padx = 29)

#sign up button
signupButton = Button(frame, text = 'Sign Up', font = ('Helvetica', 20, 'bold'), bd = 3, bg = '#800080', fg = 'white', activebackground = '#800080', activeforeground = 'white',
                      width = 19, cursor = 'hand2', command = sign_up)
signupButton.grid(row = 21, column = 0, padx = 27, pady = 30)

#have account label
account = Label(frame, text = 'Already Have An Account?', font = ('Helvetica', 11, 'bold'), fg = 'black', bg = 'white')
account.grid(row = 22, column = 0, sticky = 'w', padx = 25, pady = 5)

loginButton = Button(frame, text = 'Login', font = ('Helvetica', 11, 'bold underline'), bg = 'white', fg = 'red', bd = 0, cursor = 'hand2', activebackground = 'white', activeforeground = 'lightblue',
                     command = login_page)
loginButton.grid(row = 22, column = 1, padx = 10, pady = 10)


signup_window.mainloop()