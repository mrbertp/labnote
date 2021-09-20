from tkinter import *
from tkinter import filedialog
from wdg import *


def switch_to(new_section):

    section.winfo_children()[0].destroy()

    if new_section == 'diary':
        diary = Diary(section)
        diary.grid(row=0, column=0, sticky=S + N + E + W)

    if new_section == 'schedule':
        schedule = Schedule(section)
        schedule.grid(row=0, column=0, sticky=S + N + E + W)


root = Tk()
root.title("LabNote")
root.state('zoomed')

root.bind_all('<Escape>', lambda event: root.focus_force())

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
headers_frame = Frame(root, padx=2, pady=2, bd=2)
headers_frame.grid(row=1, column=0, sticky=E + W)

diary_header = Button(headers_frame, text='DIARY', bd=3, relief=RAISED, padx=2, pady=2, command=lambda: switch_to('diary'))
diary_header.grid(row=0, column=0)

schedule_header = Button(headers_frame, text='SCHEDULE', bd=3, relief=RAISED, padx=2, pady=2, command=lambda: switch_to('schedule'))
schedule_header.grid(row=0, column=1)

planner_header = Button(headers_frame, text='PLANNER', bd=3, relief=RAISED, padx=2, pady=2, command=lambda: switch_to('schedule'))
planner_header.grid(row=0, column=2)

# SECTION

section = LabelFrame(root, relief=SOLID)
section.grid(row=2, column=0, sticky=N + S + E + W)
section.grid_columnconfigure(0, weight=1)
section.grid_rowconfigure(0, weight=1)

diary = Diary(section)
diary.grid(row=0, column=0, sticky=S + N + E + W)

# row and column config

top_frame.grid_columnconfigure(0, weight=1)
top_frame.grid_columnconfigure(1, weight=1)
top_frame.grid_columnconfigure(2, weight=1)

root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=500)

root.mainloop()
