from tkinter import *

PHI = (1 + 5**0.5) / 2
WIDTH = int(400)
HEIGHT = int(400 * PHI)

root = Tk()
root.title("LabNote")
root.geometry(f"{WIDTH}x{HEIGHT}")


# top bar
top_frame = Frame(root, padx=4, pady=4, bg='MediumPurple1')
top_frame.grid(row=0, column=0, sticky=EW)

user_label = Label(top_frame, text="User", bd=2, relief=FLAT, padx=4, pady=4, bg='MediumPurple1')
user_label.grid(row=0, column=0, sticky=W)
date_label = Label(top_frame, text="Date", bd=2, relief=FLAT, padx=4, pady=4, bg='MediumPurple1')
date_label.grid(row=0, column=1)
time_label = Label(top_frame, text="Time", bd=2, relief=FLAT, padx=4, pady=4, bg='MediumPurple1')
time_label.grid(row=0, column=2, sticky=E)

# sections header

headers_frame = Frame(root, padx=4, pady=4, bg='DarkOrange2')
headers_frame.grid(row=1, column=0, sticky=EW)

diary_header = Button(headers_frame, text='DIARY', bd=3, relief=RAISED, padx=4, pady=2)
diary_header.grid(row=0, column=0)
schedule_header = Button(headers_frame, text='SCHEDULE', bd=3, relief=RAISED, padx=4, pady=2)
schedule_header.grid(row=0, column=1)
planner_header = Button(headers_frame, text='PLANNER', bd=3, relief=RAISED, padx=4, pady=2)
planner_header.grid(row=0, column=2)

# records

record_frame = Frame(root, padx=2, pady=2, bg='steel blue')
record_frame.grid(row=2, column=0, sticky=EW)

date = Button(record_frame, padx=2, pady=2, text='date', relief=FLAT, bd=1, bg='grey95')
date.grid(row=0, column=0)
time = Button(record_frame, padx=2, pady=2, text='time', relief=FLAT, bd=1, bg='grey95')
time.grid(row=1, column=1)
record = Entry(record_frame, bd=2, relief=FLAT)
record.grid(row=2, column=2, sticky=EW)


# row and column config
root.grid_columnconfigure(0, weight=1)
top_frame.grid_columnconfigure(0, weight=1)
top_frame.grid_columnconfigure(1, weight=1)
top_frame.grid_columnconfigure(2, weight=1)
record_frame.grid_columnconfigure(2, weight=1)

root.mainloop()
