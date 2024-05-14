from tkinter import *
from tkinter import messagebox
from PIL import ImageTk
import pymysql

def login_page():
    signup_window.destroy()
    import sign_in

def clear():
    emailEntry.delete(0, END)
    usernameEntry.delete(0, END)
    passwordEntry.delete(0, END)
    confirm_passwordEntry.delete(0, END)
    

def connect_database():
    if emailEntry.get() == '' or usernameEntry.get() == '' or passwordEntry.get() == '' or confirm_passwordEntry.get() == '':
        messagebox.showerror('Error', 'All Fields Are Required')
    elif passwordEntry.get() != confirm_passwordEntry.get():
        messagebox.showerror('Error', 'Password Does Not Match')
    else:
        try:
            con = pymysql.connect(host = 'localhost', user = 'root', password = '1234')
            mycursor = con.cursor()
        except:
            messagebox.showerror('Error', 'Database Connectivity Issue, Please Try Again')
            return
        try:
            query = 'create database userdata'
            mycursor.execute(query)
            query = 'use userdata'
            mycursor.execute(query)
            query = 'create table data(id int auto_increment primary key not null, email varchar(50), username varchar(100), password varchar(20))'
            mycursor.execute(query)
        except:
            mycursor.execute('user userdata')

        query = 'select * from data where username = %s'
        mycursor.execute(query, (usernameEntry.get()))

        row = mycursor.fetchone()
        if row != None:
            messagebox.showerror('Error', 'Username Already Exist')
        else:
            query = 'insert into data(email, username, passwrod) values(%s, %s, %s)'
            mycursor.execute(query, (emailEntry.get(), usernameEntry.get(), passwordEntry.get()))
            con.commit()
            con.close()
            messagebox.showinfo('Success', 'Registration Is Successful')
            clear()
            signup_window.destroy()
            import sign_in
        

#window setting
signup_window = Tk()
signup_window.title('Sign Up Page')
signup_window.state('zoomed')
signup_window.configure(bg = 'white')
signup_window.resizable(False, False)

frame = Frame(signup_window, bg = 'white')
frame.place(x = 800, y = 100)

heading = Label(signup_window, text = 'CREATE AN ACCOUNT', font = ('Helvetica', 23, 'bold'), bg = 'white', fg = 'black')
heading.grid(row = 0, column = 0, padx = 830, pady = 50)

#email label
emailLabel = Label(frame, text = 'Email:', font = ('Helvetica', 17), bg = 'white', fg = 'black')
emailLabel.grid(row = 7, column = 0, sticky = 'w', padx = 25)
emailEntry = Entry(frame, width = 25, font = ('Helvetica', 17), bg = 'lightblue', fg = 'black')
emailEntry.grid(row = 8, column = 0, sticky = 'w', padx = 29)

#username label
usernameLabel = Label(frame, text = 'Username:', font = ('Helvetica', 17), bg = 'white', fg = 'black')
usernameLabel.grid(row = 9, column = 0, sticky = 'w', padx = 25, pady = (10, 0))
usernameEntry = Entry(frame, width = 25, font = ('Helvetica', 17), bg = 'lightblue', fg = 'black')
usernameEntry.grid(row = 10, column = 0, sticky = 'w', padx = 29)

#password label
passwordLabel = Label(frame, text = 'Password:', font = ('Helvetica', 17), bg = 'white', fg = 'black')
passwordLabel.grid(row = 11, column = 0, sticky = 'w', padx = 25, pady = (10, 0))
passwordEntry = Entry(frame, width = 25, font = ('Helvetica', 17), bg = 'lightblue', fg = 'black')
passwordEntry.grid(row = 12, column = 0, sticky = 'w', padx = 29)

#confirm password label
confirm_passwordLabel = Label(frame, text = 'Confirm Password:', font = ('Helvetica', 17), bg = 'white', fg = 'black')
confirm_passwordLabel.grid(row = 13, column = 0, sticky = 'w', padx = 25, pady = (10, 0))
confirm_passwordEntry = Entry(frame, width = 25, font = ('Helvetica', 17), bg = 'lightblue', fg = 'black')
confirm_passwordEntry.grid(row = 14, column = 0, sticky = 'w', padx = 29)

#sign up button
signupButton = Button(frame, text = 'Sign Up', font = ('Helvetica', 20, 'bold'), bd = 0, bg = 'lightblue', fg = 'black', activebackground = 'lightblue', activeforeground = 'black',
                      width = 19, cursor = 'hand2', command = connect_database)
signupButton.grid(row = 21, column = 0, padx = 27, pady = 30)

#have account label
account = Label(frame, text = 'Already Have An Account?', font = ('Helvetica', 11, 'bold'), fg = 'black', bg = 'white')
account.grid(row = 22, column = 0, sticky = 'w', padx = 25, pady = 5)

loginButton = Button(frame, text = 'Login', font = ('Helvetica', 11, 'bold underline'), bg = 'white', fg = 'red', bd = 0, cursor = 'hand2', activebackground = 'white', activeforeground = 'red',
                     command = login_page)
loginButton.place(x = 220, y = 392)



signup_window.mainloop()