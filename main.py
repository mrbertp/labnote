from tkinter import *
import config
import datetime as dt

root = Tk()
root.title("LabNote")
root.geometry(f"{config.WIDTH}x{config.HEIGHT}")

records = []


def refresh_records(master, records):

    for i in range(len(records)):
        Record(master, i, records[i])


def add_record(master, position):

    global records
    date = dt.datetime.now().strftime("%Y/%m/%d")
    hour = dt.datetime.now().strftime("%H:%M")
    text = dt.datetime.now().strftime("%S")
    content = [date, hour, text]
    records.insert(position, content)
    print(records)
    refresh_records(master, records)


class Record():

    def __init__(self, master, position, content):

        record_frame = LabelFrame(master, padx=6, pady=6, bg='grey95', relief=FLAT, bd=2)
        record_frame.grid(row=position, column=0, sticky=EW)

        record_frame.grid_columnconfigure(0, weight=1)
        record_frame.grid_columnconfigure(1, weight=2)
        record_frame.grid_columnconfigure(2, weight=2)
        record_frame.grid_columnconfigure(3, weight=500)

        top_margin = Button(record_frame, padx=2, pady=2, relief=SOLID, bd=1, bg='grey95',
                            command=lambda: add_record(master, position))
        top_margin.grid(row=0, column=0)
        middle_margin = Button(record_frame, padx=2, pady=2, relief=SOLID, bd=1, bg='grey95')
        middle_margin.grid(row=1, column=0)
        bot_margin = Button(record_frame, padx=2, pady=2, relief=SOLID, bd=1, bg='grey95',
                            command=lambda: add_record(master, position + 1))
        bot_margin.grid(row=2, column=0)

        date = Button(record_frame, padx=2, pady=2, text=content[0], relief=FLAT, bd=1, bg='grey95')
        date.grid(row=0, column=1)
        time = Button(record_frame, padx=2, pady=2, text=content[1], relief=FLAT, bd=1, bg='grey95')
        time.grid(row=1, column=2)
        text = Entry(record_frame, bd=5, relief=FLAT)
        text.grid(row=2, column=3, sticky=EW)
        text.delete(0, END)
        text.insert(0, content[2])


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
records_frame = LabelFrame(root, padx=4, pady=4, bd=4, relief=FLAT)
records_frame.grid(row=2, column=0, sticky=EW)
records_frame.grid_columnconfigure(0, weight=1)

add_record(records_frame, position=0)


# row and column config
root.grid_columnconfigure(0, weight=1)
top_frame.grid_columnconfigure(0, weight=1)
top_frame.grid_columnconfigure(1, weight=1)
top_frame.grid_columnconfigure(2, weight=1)

root.mainloop()
