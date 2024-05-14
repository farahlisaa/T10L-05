from tkinter import *
from PIL import ImageTk
from tkinter import messagebox
import pymysql

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

def login_user():
    if usernameEntry.get() == '' or passwordEntry.get() == '':
        messagebox.showerror('Error', 'All Fields Are Required')

    else:
        try:
            con = pymysql.connect(host = 'localhost', user = 'root', password = '1234')
            mycursor = con.cursor()
        except:
            messagebox.showerror('Error', 'Connection is not established, Try Again')
            return
        query = 'use userdata'
        mycursor.execute(query)
        query = 'select * from data where username = %s and password = %s'
        mycursor.execute(query, (usernameEntry.get(), passwordEntry.get()))
        row = mycursor.fetchone()
        if row == None:
            messagebox.showerror('Error', 'Invalid Username Or Password')
        else:
            messagebox.showinfo('Success', 'Successful Login')

def forget_pass():

    def change_password():
        if user_entry.get() == '' or newpass_entry.get() == '' or confirmpass_entry.get() == '':
            messagebox.showerror('Error', 'All Fields Are Required', parent = window)
        elif newpass_entry.get() != confirmpass_entry.get():
            messagebox.showerror('Error', 'New Password Does Not Match', parent = window)
        else:
            con = pymysql.connect(host = 'localhost', user = 'root', password = '1234', database = 'userdata')
            mycursor = con.cursor()
            query = 'select * from data where username = %s'
            mycursor.execute(query, (user_enter.get()))
            row = mycursor.fetchone
            if row == None:
                messagebox.showerror('Error', 'Incorrect Username', parent = window)
            else:
                query = 'update data set password = %s'
                mycursor.execute(query, (newpass_entry.get(), user_entry.get()))
                con.commit()
                con.close()
                messagebox.showinfo('Success', 'Password is reset, please lofin with new password', parent = window)
                window.destroy()

    window = Toplevel()
    window.title('Reset Password')
    window.configure(bg = 'white')
    window.state('zoomed')
    window.resizable(False, False)

    heading_label = Label(window, text = 'RESET PASSWORD', font = ('Helvetica', 23, 'bold'), bg = 'white', fg = 'black')
    heading_label.place(x = 800, y = 100)

    userLabel = Label(window, text = 'Username', font = ('Helvetica', 11, 'bold'), bg = 'white', fg = 'black')
    userLabel.place(x = 795, y = 160)

    user_entry = Entry(window, width = 25, fg = 'black', font = ('Helvetica', 11), bd = 0)
    user_entry.place(x = 800, y = 180)

    frame_1 = Frame(window, width = 250, height = 2, bg = 'black')
    frame_1.place(x = 800, y = 200)    

    newpassLabel = Label(window, text = 'New Password', font = ('Helvetica', 11, 'bold'), bg = 'white', fg = 'black')
    newpassLabel.place(x = 795, y = 250)

    newpass_entry = Entry(window, width = 25, fg = 'black', font = ('Helvetica', 11), bd = 0)
    newpass_entry.place(x = 800, y = 270)

    frame_2 = Frame(window, width = 250, height = 2, bg = 'black')
    frame_2.place(x = 800, y = 290)

    confirmpassLabel = Label(window, text = 'Confirm Password', font = ('Helvetica', 11, 'bold'), bg = 'white', fg = 'black')
    confirmpassLabel.place(x = 795, y = 340)

    confirmpass_entry = Entry(window, width = 25, fg = 'black', font = ('Helvetica', 11), bd = 0)
    confirmpass_entry.place(x = 800, y = 360)

    frame_3 = Frame(window, width = 250, height = 2, bg = 'black')
    frame_3.place(x = 800, y = 380)

    submitButton = Button(window, text = 'Submit', bd = 0, bg = 'lightblue', fg = 'black', font = ('Helvetica', 20, 'bold'), width = 15, 
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
eyeButton = Button(window, image = openeye, bd = 0, bg = 'white', activebackground = 'white', cursor = 'hand2', comman = hide)
eyeButton.place(x = 1020, y = 200)

#forget button
forgetButton = Button(window, text = 'Forget Password?', font = ('Helvetica', 9, 'bold'), bd = 0, bg = 'white', activebackground = 'white', 
                      cursor = 'hand2', command = forget_pass)
forgetButton.place(x = 940, y = 250)

#login button
loginButton = Button(window, text = 'Login', font = ('Helvetica', 20, 'bold'), fg = 'black', bg = 'lightblue', cursor = 'hand2', bd = 0, 
                     width = 15, command = login_user)
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