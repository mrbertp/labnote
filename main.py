from tkinter import *
from wdg import *


root = Tk()
root.title("LabNote")
root.state('zoomed')

# top bar
top_frame = Frame(root, padx=2, pady=2, bd=2, relief=SOLID)
top_frame.grid(row=0, column=0, sticky=E + W)

user_label = Label(top_frame, text="User", bd=2, relief=FLAT, padx=2, pady=2)
user_label.grid(row=0, column=0, sticky=W)
date_label = Label(top_frame, text="Date", bd=2, relief=FLAT, padx=2, pady=2)
date_label.grid(row=0, column=1)
time_label = Label(top_frame, text="Time", bd=2, relief=FLAT, padx=2, pady=2)
time_label.grid(row=0, column=2, sticky=E)

# sections header
headers_frame = Frame(root, padx=2, pady=2, bd=2, relief=SOLID)
headers_frame.grid(row=1, column=0, sticky=E + W)

diary_header = Button(headers_frame, text='DIARY', bd=3, relief=RAISED, padx=2, pady=2)
diary_header.grid(row=0, column=0)
schedule_header = Button(headers_frame, text='SCHEDULE', bd=3, relief=RAISED, padx=2, pady=2)
schedule_header.grid(row=0, column=1)
planner_header = Button(headers_frame, text='PLANNER', bd=3, relief=RAISED, padx=2, pady=2)
planner_header.grid(row=0, column=2)

# DIARY

diary = Diary(root)

# row and column config
# TODO: diary records and calendar separation is not exactly at the middle of screen
top_frame.grid_columnconfigure(0, weight=1)
top_frame.grid_columnconfigure(1, weight=1)
top_frame.grid_columnconfigure(2, weight=1)

root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=500)

root.mainloop()
