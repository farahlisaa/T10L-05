from tkinter import *
from tkcalendar import *

root = Tk()
root.geometry("500x400")
root.configure(background="#0055fe")


# keying in the selected date when user closes the calendar
def pick_date(event):
    global cal, date_window

    date_window = Toplevel()
    date_window.grab_set()
    date_window.title("Choose Date")
    date_window.geometry('250x220+590+370')
    cal = Calendar(date_window, selectmode="day", date_pattern="DD/MM/YYYY")
    cal.place(x=0, y=0)

    submit_btn = Button(date_window, text="Submit", command=grab_date)
    submit_btn.place(x=80, y=190)


def grab_date():
    date_entry.delete(0, END)
    date_entry.insert(0, cal.get_date())
    date_window.destroy()


# accepting date after clicking submit
date_label = Label(root, text="Date: ", bg="#0055fe", fg="white", font=("Arial", 13, "bold"))
date_label.place(x=40, y=160)

date_entry = Entry(root, highlightthickness=0, relief=FLAT, bg="white", fg="#6b6a69", font=("Aria;", 12, "bold"))
date_entry.place(x=160, y=160, width=255)
date_entry.insert(0, "DD/MM/YYYY")
date_entry.bind("<1>", pick_date)

root.mainloop()
