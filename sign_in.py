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
window.configure(bg = 'white')
window.resizable(False, False)

heading = Label(window, text = 'USER LOGIN', font = ('Helvetica', 23, 'bold'), bg = 'white', fg = 'black')
heading.place(x = 830, y = 100)


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
            messagebox.showerror("Error", "Invalid email or password.")
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
    reset_window.configure(bg = 'white')
    reset_window.state('zoomed')
    reset_window.resizable(False, False)

    heading_label = Label(reset_window, text = 'RESET PASSWORD', font = ('Helvetica', 23, 'bold'), bg = 'white', fg = 'black')
    heading_label.place(x = 800, y = 100)

    userLabel = Label(reset_window, text = 'Username', font = ('Helvetica', 11, 'bold'), bg = 'white', fg = 'black')
    userLabel.place(x = 795, y = 160)

    user_entry = Entry(reset_window, width = 25, fg = 'black', font = ('Helvetica', 11), bd = 0)
    user_entry.place(x = 800, y = 180)

    frame_1 = Frame(reset_window, width = 250, height = 2, bg = 'black')
    frame_1.place(x = 800, y = 200)    

    newpassLabel = Label(reset_window, text = 'New Password', font = ('Helvetica', 11, 'bold'), bg = 'white', fg = 'black')
    newpassLabel.place(x = 795, y = 250)

    newpass_entry = Entry(reset_window, width = 25, fg = 'black', font = ('Helvetica', 11), bd = 0)
    newpass_entry.place(x = 800, y = 270)

    frame_2 = Frame(reset_window, width = 250, height = 2, bg = 'black')
    frame_2.place(x = 800, y = 290)

    confirmpassLabel = Label(reset_window, text = 'Confirm Password', font = ('Helvetica', 11, 'bold'), bg = 'white', fg = 'black')
    confirmpassLabel.place(x = 795, y = 340)

    confirmpass_entry = Entry(reset_window, width = 25, fg = 'black', font = ('Helvetica', 11), bd = 0)
    confirmpass_entry.place(x = 800, y = 360)

    frame_3 = Frame(reset_window, width = 250, height = 2, bg = 'black')
    frame_3.place(x = 800, y = 380)

    submitButton = Button(reset_window, text = 'Submit', bd = 0, bg = 'lightblue', fg = 'black', font = ('Helvetica', 20, 'bold'), width = 15, 
                          cursor = 'hand2', activebackground = 'lightblue', activeforeground = 'black', command = change_password)
    submitButton.place(x = 800, y = 430)


#username entry
usernameEntry = Entry(window, width = 25, font = ('Helvetica', 11, 'bold'), bd = 0, fg = 'black')
usernameEntry.place(x = 800, y = 160)
usernameEntry.insert(0, 'Username')
usernameEntry.bind('<FocusIn>', user_enter)

frame_1 = Frame(window, width = 250, height = 2, bg = 'black')
frame_1.place(x = 800, y = 180)

#password entry
passwordEntry = Entry(window, width = 25, font = ('Helvetica', 11, 'bold'), bd = 0, fg = 'black')
passwordEntry.place(x = 800, y = 210)
passwordEntry.insert(0, 'Password')
passwordEntry.bind('<FocusIn>', password_enter)

frame_2 = Frame(window, width = 250, height = 2, bg = 'black')
frame_2.place(x = 800, y = 230)

#eye button
openeye = PhotoImage(file = 'openeye.png')
eyeButton = Button(window, image = openeye, bd = 0, bg = 'white', activebackground = 'white', cursor = 'hand2', command = hide)
eyeButton.place(x = 1020, y = 200)

#forget button
forgetButton = Button(window, text = 'Forget Password?', font = ('Helvetica', 9, 'bold'), bd = 0, bg = 'white', activebackground = 'white', 
                      cursor = 'hand2', command = forget_pass)
forgetButton.place(x = 940, y = 250)

#login button
loginButton = Button(window, text = 'Login', font = ('Helvetica', 20, 'bold'), fg = 'black', bg = 'lightblue', cursor = 'hand2', bd = 0, 
                     width = 15, command = sign_in)
loginButton.place(x = 800, y = 300)

#or label
orLabel = Label(window, text = '----------- OR -----------', font = ('Helvetica', 20), fg = 'black', bg = 'white')
orLabel.place(x = 800, y = 380)

#sign up/new account
signupLabel = Label(window, text = "Don't Have An Account?", font = ('Helvetica', 9, 'bold'), fg = 'black', bg = 'white')
signupLabel.place(x = 800, y = 450)

newaccButton = Button(window, text = 'Create New Account!', font = ('Helvetica', 9, 'bold underline'), fg = 'red', bg = 'white', activeforeground = 'lightblue', activebackground = 'white',cursor = 'hand2', bd = 0,
                      command = signup_page)
newaccButton.place(x = 940, y = 450)


window.mainloop()