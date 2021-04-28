from tkinter import *
import config
import datetime as dt


class Record(LabelFrame):

    def __init__(self, parent, grandparent, position, content):

        self.parent = parent
        self.grandparent = grandparent
        self.position = position
        self.content = content

        LabelFrame.__init__(self, self.parent, padx=10, pady=10, relief=FLAT, bd=5)

        self.top_button = Button(self, padx=2, pady=2, relief=SOLID, bd=1, width=2, height=1, text='^',
                                 command=lambda: self.add_record(position))
        self.top_button.grid(row=0, column=0, sticky=W)

        self.middle_button = Button(self, padx=2, pady=2, relief=SOLID, bd=1, width=2, height=1, text='x',
                                    command=lambda: self.delete_record(position))
        self.middle_button.grid(row=1, column=0, sticky=W)

        self.bot_button = Button(self, padx=2, pady=2, relief=SOLID, bd=1, width=2, height=1, text='v',
                                 command=lambda: self.add_record(position + 1))
        self.bot_button.grid(row=2, column=0, sticky=W)

        self.date = Button(self, padx=2, pady=2, text=content[0], relief=FLAT, bd=1, width=10)
        self.date.grid(row=0, column=1, sticky=E + W)
        self.time = Button(self, padx=2, pady=2, text=content[1], relief=FLAT, bd=1, width=10)
        self.time.grid(row=1, column=1, sticky=E + W)
        # it is better to use Text widget
        self.text = Text(self, bd=5, relief=FLAT, height=5, padx=2, pady=2)
        self.text.configure(font=("Arial", 10, "normal"))
        self.text.grid(row=0, column=2, rowspan=3, sticky=W + E)
        self.text.insert(INSERT, content[2])

        self.grid(row=position, column=0, sticky=W + E)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(2, weight=100)

    def refresh_records(self):

        if len(self.grandparent.records) == 0:

            Record(diary_records.frame, diary_records, position=0, content=['-', '-', '-'])

        else:

            self.parent.destroy()
            self.grandparent.load()

            for i in range(len(self.grandparent.records)):
                Record(self.grandparent.frame, self.grandparent, i, self.grandparent.records[i])

            self.grandparent.conf()

    def add_record(self, position):

        date = dt.datetime.now().strftime("%Y/%m/%d")
        hour = dt.datetime.now().strftime("%H:%M")
        text = dt.datetime.now().strftime("%S")
        content = [date, hour, text]
        self.grandparent.records.insert(position, content)
        self.refresh_records()

    def delete_record(self, position):

        if len(self.grandparent.records) != 0:

            self.grandparent.records.remove(self.grandparent.records[position])
            self.refresh_records()


class Diary_Records(LabelFrame):

    def __init__(self, parent):

        self.parent = parent
        self.records = []

        LabelFrame.__init__(self, self.parent, padx=0, pady=0, bd=2, relief=SOLID)

    def load(self):

        self.canvas = Canvas(self, bd=0, relief=SOLID)
        self.canvas.grid(row=0, column=0, sticky=N + S + E + W)

        self.scrollbar = Scrollbar(self, orient='vertical', command=self.canvas.yview)
        # self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row=0, column=1, sticky=N + S)

        self.frame = LabelFrame(self.canvas, padx=0, pady=0, bd=0, relief=SOLID)
        self.frame.grid(row=0, column=0, sticky=E + W)
        self.frame.grid_columnconfigure(0, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def conf(self):

        self.canvas.create_window((0, 0), window=self.frame, anchor="nw", tags="my_tag")
        self.frame.bind("<Configure>", self.config_frame)
        self.canvas.bind("<Configure>", self.config_canvas)
        self.bind_all("<MouseWheel>", self.mouse_scroll)

    def config_frame(self, event):

        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def config_canvas(self, event):

        self.canvas.itemconfigure("my_tag", width=event.width - 8)

    def mouse_scroll(self, event):

        self.canvas.yview_scroll(int(-1 * event.delta / 120), "units")


class Calendar(LabelFrame):

    def __init__(self, parent):

        self.parent = parent

        LabelFrame.__init__(self, self.parent, padx=10, pady=10, bd=2, relief=SOLID)

        self.year = Frame(self, padx=5, pady=5)
        self.year.grid(row=0, column=0, sticky=N + S + W + E)
        self.year.grid_columnconfigure(0, weight=1)
        self.year.grid_columnconfigure(2, weight=1)

        self.previous_year = Button(self.year, relief=SOLID, text='<', width=4, heigh=1)
        self.previous_year.grid(row=0, column=0, sticky=E)

        self.show_year = dt.datetime.now().strftime("%Y")
        self.year_button = Button(self.year, relief=SOLID, text=self.show_year, width=10, height=1)
        self.year_button.grid(row=0, column=1)

        self.next_year = Button(self.year, relief=SOLID, text='>', width=4, heigh=1)
        self.next_year.grid(row=0, column=2, sticky=W)

        self.month = Frame(self, padx=10, pady=10)
        self.month.grid(row=1, column=0, sticky=N + S + E + W)

        self.month.grid_columnconfigure(0, weight=1)
        self.month.grid_columnconfigure(2, weight=1)

        self.previous_month = Button(self.month, relief=SOLID, text='<', width=4, heigh=1, command=lambda: self.update_calendar(-1))
        self.previous_month.grid(row=0, column=0, sticky=E)

        self.show_month = int(dt.datetime.now().strftime("%m"))
        self.month_button = Button(self.month, relief=SOLID, text=config.months[self.show_month - 1], width=10, height=1)
        self.month_button.grid(row=0, column=1)

        self.next_month = Button(self.month, relief=SOLID, text='>', width=4, heigh=1, command=lambda: self.update_calendar(1))
        self.next_month.grid(row=0, column=2, sticky=W)

        self.load_days()

    def load_days(self):

        self.days = Frame(self, padx=10, pady=10)
        self.days.grid(row=2, column=0)
        for i in range(7):
            self.days.grid_columnconfigure(i, weight=1)

        for i in range(1, config.month_dict[config.months[self.show_month - 1]] + 1):

            self.day_button = Button(self.days, relief=SOLID, text=i, height=2, width=6)
            self.day_button.grid(row=((i + config.week_scheme[self.show_month - 1]) // 7 - 1) if ((i + config.week_scheme[self.show_month - 1]) % 7 == 0) else ((i + config.week_scheme[self.show_month - 1]) // 7),
                                 column=6 if ((i + config.week_scheme[self.show_month - 1]) % 7 == 0) else ((i + config.week_scheme[self.show_month - 1]) % 7 - 1))

    def update_calendar(self, direction):

        self.show_month += direction

        self.month_button['text'] = config.months[self.show_month - 1]

        self.days.destroy()
        self.load_days()


root = Tk()
root.title("LabNote")
root.state('zoomed')

# top bar
top_frame = Frame(root, padx=2, pady=2, bd=2, relief=SOLID)
top_frame.grid(row=0, column=0, columnspan=2, sticky=E + W)

user_label = Label(top_frame, text="User", bd=2, relief=FLAT, padx=2, pady=2)
user_label.grid(row=0, column=0, sticky=W)
date_label = Label(top_frame, text="Date", bd=2, relief=FLAT, padx=2, pady=2)
date_label.grid(row=0, column=1)
time_label = Label(top_frame, text="Time", bd=2, relief=FLAT, padx=2, pady=2)
time_label.grid(row=0, column=2, sticky=E)

# sections header
headers_frame = Frame(root, padx=2, pady=2, bd=2, relief=SOLID)
headers_frame.grid(row=1, column=0, columnspan=2, sticky=E + W)

diary_header = Button(headers_frame, text='DIARY', bd=3, relief=RAISED, padx=2, pady=2)
diary_header.grid(row=0, column=0)
schedule_header = Button(headers_frame, text='SCHEDULE', bd=3, relief=RAISED, padx=2, pady=2)
schedule_header.grid(row=0, column=1)
planner_header = Button(headers_frame, text='PLANNER', bd=3, relief=RAISED, padx=2, pady=2)
planner_header.grid(row=0, column=2)

# DIARY

# calendar

diary_calendar = Calendar(root)
diary_calendar.grid(row=2, column=0, sticky=E + W + N + S)
diary_calendar.grid_columnconfigure(0, weight=1)

# records
diary_records = Diary_Records(root)
diary_records.load()
diary_records.grid(row=2, column=1, sticky=E + W + N + S)

record = Record(diary_records.frame, diary_records, position=0, content=['-', '-', '-'])
record.grid(row=0, column=0, sticky=E + W)

diary_records.conf()

# row and column config
# TODO: diary records and calendar separation is not exactly at the middle of screen
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=10)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1000)
top_frame.grid_columnconfigure(0, weight=1)
top_frame.grid_columnconfigure(1, weight=1)
top_frame.grid_columnconfigure(2, weight=1)

root.mainloop()
