from tkinter import *
import cfg
import datetime as dt


class Panel(LabelFrame):

    def __init__(self, parent):

        self.parent = parent

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

        self.canvas.create_window((0, 0), window=self.frame, anchor="nw", tags="canvas")
        self.frame.bind("<Configure>", self.config_frame)
        self.canvas.bind("<Configure>", self.config_canvas)
        self.bind_all("<MouseWheel>", self.mouse_scroll)

    def config_frame(self, event):

        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def config_canvas(self, event):

        self.canvas.itemconfigure("canvas", width=event.width - 8)

    def mouse_scroll(self, event):

        self.canvas.yview_scroll(int(-1 * event.delta / 120), "units")


class Record(LabelFrame):

    def __init__(self, head, position, content):

        self.head = head
        self.position = position
        self.content = content

        LabelFrame.__init__(self, self.head.panel.frame, padx=10, pady=10, relief=FLAT, bd=5)

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
        self.text = Text(self, bd=5, relief=FLAT, height=5, padx=2, pady=2)
        self.text.configure(font=("Arial", 10, "normal"))
        self.text.grid(row=0, column=2, rowspan=3, sticky=W + E)
        self.text.insert(INSERT, content[2])

        self.grid(row=position, column=0, sticky=W + E)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(2, weight=100)

    def add_record(self, position):

        date = self.head.calendar.selected_date
        hour = dt.datetime.now().strftime("%H:%M")
        text = ''
        content = [date, hour, text]

        if self.head.calendar.selected_date in self.head.records.keys():

            self.head.save_records()
            self.head.records[self.head.calendar.selected_date].insert(position, content)

        else:
            self.head.records[self.head.calendar.selected_date] = [content]

        self.head.refresh_records()

    def delete_record(self, position):

        if self.head.calendar.selected_date in self.head.records.keys():
            if len(self.head.records[self.head.calendar.selected_date]) > 1:
                self.head.save_records()
                del self.head.records[self.head.calendar.selected_date][position]
            else:
                del self.head.records[self.head.calendar.selected_date]
            self.head.refresh_records()


class Calendar(LabelFrame):

    def __init__(self, parent):

        self.parent = parent

        LabelFrame.__init__(self, self.parent, padx=10, pady=10, bd=2, relief=SOLID)

        self.today = dt.datetime.now().strftime("%Y/%m/%d").split("/")
        self.selected_date = '/'.join(self.today)

        self.year = Frame(self, padx=10, pady=10)
        self.year.grid(row=0, column=0, sticky=N)
        self.year.grid_columnconfigure(0, weight=1)
        self.year.grid_columnconfigure(2, weight=1)

        self.previous_year = Button(self.year, relief=SOLID, text='<', width=4, heigh=1)
        self.previous_year.grid(row=0, column=0, sticky=E)

        self.year_to_show = int(self.today[0])
        self.year_button = Button(self.year, relief=SOLID, text=self.year_to_show, width=10, height=1)
        self.year_button.grid(row=0, column=1)

        self.next_year = Button(self.year, relief=SOLID, text='>', width=4, heigh=1)
        self.next_year.grid(row=0, column=2, sticky=W)

        self.month = Frame(self, padx=10, pady=10)
        self.month.grid(row=1, column=0, sticky=N)

        self.month.grid_columnconfigure(0, weight=1)
        self.month.grid_columnconfigure(2, weight=1)

        self.previous_month = Button(self.month, relief=SOLID, text='<', width=4, heigh=1, command=lambda: self.update_display(-1))
        self.previous_month.grid(row=0, column=0, sticky=E)

        self.month_to_show = int(self.today[1])
        self.month_button = Button(self.month, relief=SOLID, text=cfg.months[self.month_to_show - 1], width=10, height=1)
        self.month_button.grid(row=0, column=1)

        self.next_month = Button(self.month, relief=SOLID, text='>', width=4, heigh=1, command=lambda: self.update_display(1))
        self.next_month.grid(row=0, column=2, sticky=W)

        self.load_days()

        self.grid(row=1, column=0, sticky=W + N + S)

    def load_days(self):

        self.days = Frame(self, padx=10, pady=10, bd=2, relief=SOLID)
        self.days.grid(row=2, column=0)

        for i in range(7):

            self.days.grid_columnconfigure(i, weight=1)

        for i in range(1, cfg.month_dict[cfg.months[self.month_to_show - 1]] + 1):

            self.is_today = (self.year_to_show == int(self.today[0])) and (self.month_to_show == int(self.today[1])) and (i == int(self.today[2]))
            self.day_button = Button(self.days,
                                     relief=SOLID,
                                     bg='black' if self.is_today else '#F0F0F0',
                                     fg='white' if self.is_today else 'black',
                                     text=i,
                                     command=lambda day=i: self.update_selected(day),
                                     height=2, width=6)
            self.day_button.grid(row=((i + cfg.week_scheme[self.month_to_show - 1]) // 7 - 1) if ((i + cfg.week_scheme[self.month_to_show - 1]) % 7 == 0) else ((i + cfg.week_scheme[self.month_to_show - 1]) // 7),
                                 column=6 if ((i + cfg.week_scheme[self.month_to_show - 1]) % 7 == 0) else ((i + cfg.week_scheme[self.month_to_show - 1]) % 7 - 1))

    def update_display(self, direction):

        self.month_to_show += direction

        self.month_button['text'] = cfg.months[self.month_to_show - 1]

        self.days.destroy()
        self.load_days()

    def update_selected(self, day):

        # TODO: highlight the selected day by changing the background color
        self.parent.save_records()
        date_string = list(map(str, [self.year_to_show, self.month_to_show, day]))
        date_padded = list(map(lambda s: s.rjust(2, "0"), date_string))
        self.selected_date = '/'.join(date_padded)
        self.parent.refresh_records()


class Diary(LabelFrame):

    def __init__(self, parent):

        self.parent = parent
        self.records = {}

        LabelFrame.__init__(self, self.parent, bd=2, relief=SOLID)

        self.save_button = Button(self, text='Save', command=self.save_records)
        self.save_button.grid(row=0, column=0, sticky=W)

        self.calendar = Calendar(self)

        self.panel = Panel(self)
        self.panel.load()
        self.panel.grid(row=1, column=1, sticky=N + S + E + W)

        self.load_records()

        self.refresh_records()

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.grid(row=2, column=0, sticky=S + N + E + W)

    def save_records(self):

        # TODO: sort records by date before saving into file
        if self.calendar.selected_date in self.records.keys():

            self.records[self.calendar.selected_date] = []

            for child in self.panel.frame.winfo_children():
                new_text = child.text.get("1.0", "end-1c")
                self.records[self.calendar.selected_date].append([child.content[0], child.content[1], new_text])

            with open('records.txt', 'w') as file:
                file.write('-----\n')
                for i in self.records.keys():
                    file.write('\n')
                    for j in self.records[i]:
                        file.write('>' + ';'.join(j) + '\n')
                    file.write('>-----\n')

    def load_records(self):

        self.records = {}

        try:
            with open('records.txt', 'r') as file:
                file_content = file.read()
                days = file_content.split('-----\n')
                for day in days:
                    if day != '':
                        aux = []
                        entries = day.split('\n>')
                        for entry in entries:
                            if entry != '':
                                aux.append(entry.split(';'))
                        date = aux[0][0]
                        self.records[date] = aux
        except:
            open('records.txt', 'w').close()

        for k in self.records.keys():
            print(k, self.records[k])

    def refresh_records(self):

        self.panel.frame.destroy()
        self.panel.load()

        if self.calendar.selected_date in self.records.keys():

            for i in range(len(self.records[self.calendar.selected_date])):
                Record(self, i, self.records[self.calendar.selected_date][i])

        else:

            Record(self, position=0, content=['-', '-', 'Press the "^" button to add a Record above\nPress the "v" button to add a Record below'])

        self.panel.conf()
