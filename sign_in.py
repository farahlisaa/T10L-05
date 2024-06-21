from tkinter import *
from tkinter import messagebox
import sqlite3

def signup_page():
    window.destroy()
    import sign_up

#window setting
window = Tk()
window.title("Sign In Page")
window.state('zoomed')
window.configure(bg = '#FCC0CB')


frame = Frame(window, bg = 'white')
frame.grid(padx = 20, pady = 20)

heading = Label(frame, text = 'USER LOGIN', font = ('Helvetica', 23, 'bold'), bg = 'white', fg = 'black')
heading.grid(row = 0, column = 0, padx = 50, pady = 10)

#logo
logo = PhotoImage(file = 'logo.png')
app_logo = Label(window, image = logo, bd = 3, bg =  'white')
app_logo.place(x = 500, y = 25)

#database
def sign_in():
    username = usernameEntry.get()
    password = passwordEntry.get()

    try:
        connect = sqlite3.connect('user_data.db')
        c = connect.cursor()

        c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
        user = c.fetchone()

        if user:
            messagebox.showinfo("Success", "Login successful!")
        else:
            messagebox.showerror("Error", "Invalid username or password.")
            return
        connect.close()

    except sqlite3.Error as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

    window.destroy()

#functionality part
def user_enter(event):
    if usernameEntry.get() == 'Username':
        usernameEntry.delete(0, END)

def password_enter(event):
    if passwordEntry.get() == 'Password':
        passwordEntry.delete(0, END)

def hide():
    openeye.config(file = 'closeye.png')
    passwordEntry.config(show = '*')
    eyeButton.config(command = show)

def show():
    openeye.config(file = 'openeye.png')
    passwordEntry.config(show = '')
    eyeButton.config(command = hide)

def forget_pass():

    def change_password():
        username = user_entry.get()
        new_password = newpass_entry.get()
        confirm_password = confirmpass_entry.get()

        if username == '' or new_password == '' or confirm_password == '':
            messagebox.showerror('Error', 'All Fields Are Required', parent = reset_window)
        elif new_password != confirm_password:
            messagebox.showerror('Error', 'New Password Does Not Match', parent = reset_window)
        else:
            try:
                connect = sqlite3.connect('user_data.db')
                c = connect.cursor()

                c.execute('SELECT * FROM users WHERE username=?', (username,))
                user = c.fetchone()

                if user:
                    c.execute('UPDATE users SET password=? WHERE username=?', (new_password, username))
                    connect.commit()
                    messagebox.showinfo('Success', 'Password is reset, please login with new password', parent = reset_window)
                    reset_window.destroy()
                else:
                    messagebox.showerror('Error', 'Username not found', parent = reset_window)

                connect.close()
            except sqlite3.Error as e:
                messagebox.showerror('Error', f'An error occurred: {e}', parent = reset_window)

#reset password page
    reset_window = Toplevel()
    reset_window.title('Reset Password')
    reset_window.configure(bg = '#FCC0CB')
    reset_window.state('zoomed')

    reset_frame = Frame(reset_window, bg = '#800080')
    reset_frame.pack(pady = 20)

    heading_label = Label(reset_frame, text = 'RESET PASSWORD', font = ('Helvetica', 23, 'bold'), bg = '#800080', fg = 'white')
    heading_label.grid(row = 0, column = 0, padx = 10, pady = 10)

    userLabel = Label(reset_frame, text = 'Username:', font = ('Helvetica', 11, 'bold'), bg = '#800080', fg = 'white')
    userLabel.grid(row = 1, column = 0, padx = 10, pady = 10)

    user_entry = Entry(reset_frame, width = 25, fg = 'black', bg = 'white', font = ('Helvetica', 11, 'bold'), bd = 0)
    user_entry.grid(row = 1, column = 1, padx = 10, pady = 10)

    newpassLabel = Label(reset_frame, text = 'New Password:', font = ('Helvetica', 11, 'bold'), bg = '#800080', fg = 'white')
    newpassLabel.grid(row = 2, column = 0, padx = 10, pady = 10)

    newpass_entry = Entry(reset_frame, width = 25, fg = 'black', bg = 'white', font = ('Helvetica', 11, 'bold'), bd = 0)
    newpass_entry.grid(row = 2, column = 1, padx = 10, pady = 10)

    confirmpassLabel = Label(reset_frame, text = 'Confirm Password:', font = ('Helvetica', 11, 'bold'), bg = '#800080', fg = 'white')
    confirmpassLabel.grid(row = 3, column = 0, padx = 10, pady = 10)

    confirmpass_entry = Entry(reset_frame, width = 25, fg = 'black', bg = 'white', font = ('Helvetica', 11, 'bold'), bd = 0)
    confirmpass_entry.grid(row = 3, column = 1, padx = 10, pady = 10)

    submitButton = Button(reset_frame, text = 'Submit', bd = 0, bg = '#FCC0CB', fg = 'black', font = ('Helvetica', 20, 'bold'), width = 15, 
                          cursor = 'hand2', activebackground = '#FCC0CB', activeforeground = 'black', command = change_password)
    submitButton.grid(row = 4, column = 1, padx = 10, pady = 10)


#username entry
usernameEntry = Entry(frame, width = 25, font = ('Helvetica', 11, 'bold'), bd = 0, fg = 'black', bg = 'white')
usernameEntry.grid(row = 1, column = 0, padx = 10, pady = 10)
usernameEntry.insert(0, 'Username')
usernameEntry.bind('<FocusIn>', user_enter)

frame_1 = Frame(window, width = 200, height = 2, bg = 'black')
frame_1.place(x = 65, y = 110)

#password entry
passwordEntry = Entry(frame, width = 25, font = ('Helvetica', 11, 'bold'), bd = 0, fg = 'black', bg = 'white')
passwordEntry.grid(row = 2, column = 0, padx = 10, pady = 10)
passwordEntry.insert(0, 'Password')
passwordEntry.bind('<FocusIn>', password_enter)

frame_2 = Frame(window, width = 200, height = 2, bg = 'black')
frame_2.place(x = 65, y = 150)

#eye button
openeye = PhotoImage(file = 'openeye.png')
eyeButton = Button(window, image = openeye, bd = 0, bg = 'white', activebackground = 'white', cursor = 'hand2', command = hide)
eyeButton.place(x = 265, y = 123)

#forget button
forgetButton = Button(frame, text = 'Forget Password?', font = ('Helvetica', 9, 'bold underline'), bd = 0, bg = 'white', activebackground = '#800080', 
                      cursor = 'hand2', command = forget_pass)
forgetButton.grid(row = 4, column = 0, padx = 10, pady = 10)

#login button
loginButton = Button(frame, text = 'Login', font = ('Helvetica', 20, 'bold'), fg = 'black', bg = '#FCC0CB', cursor = 'hand2', bd = 0, 
                     width = 15, command = sign_in)
loginButton.grid(row = 5, column = 0, padx = 10, pady = 10)

#or label
orLabel = Label(frame, text = '----------- OR -----------', font = ('Helvetica', 20), fg = 'black', bg = 'white')
orLabel.grid(row = 6, column = 0, padx = 20, pady = 10)

#sign up/new account
signupLabel = Label(frame, text = "Don't Have An Account?", font = ('Helvetica', 9, 'bold'), fg = 'black', bg = 'white')
signupLabel.grid(row = 7, column = 0, padx = 10, pady = 10)

newaccButton = Button(frame, text = 'Create New Account!', font = ('Helvetica', 9, 'bold underline'), fg = 'red', bg = 'white', activeforeground = 'lightblue', activebackground = 'white',cursor = 'hand2', bd = 0,
                      command = signup_page)
newaccButton.grid(row = 7, column = 1, padx = 10, pady = 10)


window.mainloop()