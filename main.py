from tkinter import *
import config
import datetime as dt


class Record(LabelFrame):

    def __init__(self, parent, grandparent, position, content):

        self.parent = parent
        self.grandparent = grandparent
        self.position = position
        self.content = content

        LabelFrame.__init__(self, self.parent, padx=6, pady=6, bg='grey95', relief=SOLID, bd=2, text='record')

        self.top_button = Button(self, padx=2, pady=2, relief=SOLID, bd=1, bg='grey95', width=2, height=1, text='^',
                                 command=lambda: self.add_record(position))
        self.top_button.grid(row=0, column=0, sticky=W)

        self.middle_button = Button(self, padx=2, pady=2, relief=SOLID, bd=1, bg='grey95', width=2, height=1, text='x',
                                    command=lambda: self.delete_record(position))
        self.middle_button.grid(row=1, column=0, sticky=W)

        self.bot_button = Button(self, padx=2, pady=2, relief=SOLID, bd=1, bg='grey95', width=2, height=1, text='v',
                                 command=lambda: self.add_record(position + 1))
        self.bot_button.grid(row=2, column=0, sticky=W)

        self.date = Button(self, padx=2, pady=2, text=content[0], relief=FLAT, bd=1, bg='grey95')
        self.date.grid(row=0, column=1, sticky=W)
        self.time = Button(self, padx=2, pady=2, text=content[1], relief=FLAT, bd=1, bg='grey95')
        self.time.grid(row=1, column=2, sticky=W)
        self.text = Entry(self, bd=5, relief=FLAT)
        self.text.grid(row=2, column=3, sticky=E + W)
        self.text.delete(0, END)
        self.text.insert(0, content[2])

        self.grid(row=position, column=0, sticky=W + E)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(2, weight=2)
        self.grid_columnconfigure(3, weight=50)

    def refresh_records(self):

        if len(self.grandparent.records) == 0:

            Record(diary_panel.frame, diary_panel, position=0, content=['-', '-', '-'])

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
        print(self.grandparent.records)
        self.refresh_records()

    def delete_record(self, position):

        if len(self.grandparent.records) != 0:

            self.grandparent.records.remove(self.grandparent.records[position])
            print(self.grandparent.records)
            self.refresh_records()


class Diary_Panel(LabelFrame):

    def __init__(self, parent):

        self.parent = parent
        self.records = []

        LabelFrame.__init__(self, self.parent, padx=5, pady=5, bd=5, relief=SOLID, text=" diary panel ")

    def load(self):

        self.canvas = Canvas(self, bd=2, bg="blue")
        self.canvas.grid(row=0, column=0, sticky=N + S + E + W)

        self.scrollbar = Scrollbar(self, orient='vertical', command=self.canvas.yview)
        # self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row=0, column=1, sticky=N + S)

        self.frame = LabelFrame(self.canvas, padx=5, pady=5, bd=5, relief=SOLID, text=" inner frame ")
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


root = Tk()
root.title("LabNote")
root.geometry(f"{config.WIDTH}x{config.HEIGHT}")

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

# diary

diary_panel = Diary_Panel(root)
diary_panel.load()
diary_panel.grid(row=2, column=0, sticky=N + S + E + W)

record = Record(diary_panel.frame, diary_panel, position=0, content=['-', '-', '-'])
record.grid(row=0, column=0, sticky=E + W)

diary_panel.conf()

# row and column config
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1000)
top_frame.grid_columnconfigure(0, weight=1)
top_frame.grid_columnconfigure(1, weight=1)
top_frame.grid_columnconfigure(2, weight=1)

root.mainloop()
