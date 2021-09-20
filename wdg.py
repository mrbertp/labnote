from tkinter import *
from PIL import ImageTk, Image
import cfg
import datetime as dt
import math


class Panel(LabelFrame):

    def __init__(self, parent):

        self.parent = parent

        LabelFrame.__init__(self, self.parent, padx=0, pady=0, bd=2)

    def load(self):

        self.canvas = Canvas(self, bd=0)
        self.canvas.grid(row=0, column=0, sticky=N + S + E + W)

        self.scrollbar = Scrollbar(self, orient='vertical', command=self.canvas.yview)
        # self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row=0, column=1, sticky=N + S)

        self.frame = LabelFrame(self.canvas, padx=0, pady=0, bd=0)
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

        LabelFrame.__init__(self, self.head.panel.frame, padx=10, pady=10, relief=FLAT, bd=2)

        self.top_button = Button(self, padx=2, pady=2, relief=SOLID, bd=1, width=2, height=1, text='^',
                                 command=lambda: self.add_record(position))
        self.top_button.grid(row=0, column=0, sticky=W)

        self.middle_button = Button(self, padx=2, pady=2, relief=SOLID, bd=1, width=2, height=1, text='x',
                                    command=lambda: self.delete_record(position))
        self.middle_button.grid(row=1, column=0, sticky=W)

        self.bot_button = Button(self, padx=2, pady=2, relief=SOLID, bd=1, width=2, height=1, text='v',
                                 command=lambda: self.add_record(position + 1))
        self.bot_button.grid(row=2, column=0, sticky=W)

        self.date = Entry(self, justify=CENTER, bd=0, width=10, bg='#F0F0F0')
        self.date.insert(0, content[0])
        self.date.grid(row=0, column=1, sticky=E + W)

        self.time = Entry(self, justify=CENTER, bd=0, width=10, bg='#F0F0F0')
        self.time.insert(0, content[1])
        self.time.grid(row=1, column=1, sticky=E + W)

        self.text = Text(self, wrap=WORD, bd=5, relief=FLAT, height=5, padx=2, pady=2)
        self.text.configure(font=("Courier New", 10, "normal"))
        self.text.grid(row=0, column=2, rowspan=3, sticky=W + E)
        self.text.insert(INSERT, content[2])
        self.min_lines = 5
        self.chars_line = 124

        self.images = content[3]

        pic_icon = PhotoImage(file='img\\picture_icon.png').subsample(3, 3)
        pic_label = Label(image=pic_icon)
        self.pic_button = Button(self, image=pic_icon, command=self.open_images, relief=SOLID)
        self.pic_button.grid(row=2, column=1, sticky=W)
        pic_label.image = pic_icon

        self.grid(row=position, column=0, sticky=W + E)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(2, weight=100)

        self.bind_all('<Key>', self.config_record)

    def config_record(self, event):

        self.num_lines_chars = math.ceil(len(self.text.get('1.0', 'end-1c')) / self.chars_line)
        self.num_lines_returns = len(self.text.get('1.0', 'end-1c').split('\n'))
        if (self.num_lines_chars > self.min_lines):
            self.text.configure(height=self.num_lines_chars)
        elif (self.num_lines_returns > self.min_lines):
            self.text.configure(height=self.num_lines_returns)
        else:
            self.text.configure(height=self.min_lines)

    def add_record(self, position):

        date = self.head.calendar.selected_date
        hour = dt.datetime.now().strftime("%H:%M")
        text = ''
        images = []
        content = [date, hour, text, images]

        if self.head.calendar.selected_date in self.head.records.keys():

            self.head.save_records()
            self.head.records[self.head.calendar.selected_date].insert(position, content)

        else:
            self.head.records[self.head.calendar.selected_date] = [content]

        self.head.refresh_records()

    def delete_record(self, position):

        # I cannot save records after deleting all records from a day
        if self.head.calendar.selected_date in self.head.records.keys():
            if len(self.head.records[self.head.calendar.selected_date]) > 1:
                self.head.save_records()
                del self.head.records[self.head.calendar.selected_date][position]
            else:
                del self.head.records[self.head.calendar.selected_date]
            self.head.refresh_records()

    def open_images(self):

        self.img_window = Toplevel(self)
        self.img_window.grab_set()
        self.img_window.title('Record Images')
        self.img_window.geometry('1200x600')

        self.active_img = ''

        self.load_images()

    def add_image(self):

        filename = filedialog.askopenfilename(initialdir='C\\Users\\Bert\\Desktop')
        self.images.append(filename)
        self.active_img = self.images[-1]
        self.reload_images()

    def remove_image(self):

        if len(self.images) > 1:
            self.images.remove(self.active_img)
            self.active_img = self.images[-1]

        elif len(self.images) == 1:
            self.images.remove(self.active_img)
            self.active_img = ''

        self.reload_images()

    def load_images(self):

        self.img_window_frame = Frame(self.img_window, padx=10, pady=10, relief=SOLID)
        self.img_window_frame.grid(row=0, column=0)

        self.images_names = Frame(self.img_window_frame, padx=10, pady=10, relief=SOLID)
        self.images_names.grid(row=0, column=0)

        self.images_display = Frame(self.img_window_frame, padx=10, pady=10, relief=SOLID)
        self.images_display.grid(row=0, column=1)

        self.images_actions = Frame(self.img_window_frame, padx=10, pady=10, relief=SOLID)
        self.images_actions.grid(row=1, column=0)
        Button(self.images_actions, text='Add', command=self.add_image).grid(row=0, column=0)
        Button(self.images_actions, text='Remove', command=self.remove_image).grid(row=0, column=1)

        if len(self.images) == 0:
            self.active_img = ''
            Label(self.images_names, text='No images in this record', anchor='w').grid(row=0, column=0, sticky=W)
        else:
            for i in range(len(self.images)):
                Button(self.images_names, text=self.images[i].split('/')[-1], command=lambda name=self.images[i]: self.switch_image(name)).grid(row=i, column=0, sticky=W)

        if self.active_img != '':
            self.display_image()
        else:
            Label(self.images_display, text='No image selected').grid(row=0, column=0)

    def reload_images(self):

        self.img_window_frame.destroy()
        self.load_images()

    def switch_image(self, name):

        self.active_img = name
        self.reload_images()

    def display_image(self):

        img_open = Image.open(self.active_img)
        img_load = ImageTk.PhotoImage(img_open)
        self.img_label = Label(self.images_display, image=img_load)
        self.img_label.grid(row=0, column=0)
        self.img_label.image = img_load


class Calendar(LabelFrame):

    def __init__(self, parent):

        self.parent = parent

        LabelFrame.__init__(self, self.parent, padx=10, pady=10, bd=2)

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

    def load_days(self):

        self.days = Frame(self, padx=10, pady=10, bd=2, relief=SOLID)
        self.days.grid(row=2, column=0)

        for i in range(len(cfg.week_days)):

            self.week_day = Label(self.days,
                                  text=cfg.week_days[i],
                                  font='Arial 9 bold',
                                  height=2,
                                  width=6,
                                  padx=0, pady=0,
                                  anchor=N)

            self.week_day.grid(row=0, column=i)

        for i in range(1, cfg.month_dict[cfg.months[self.month_to_show - 1]] + 1):

            self.is_today = (self.year_to_show == int(self.today[0])) and (self.month_to_show == int(self.today[1])) and (i == int(self.today[2]))
            self.is_selected = '/'.join(list(map(lambda s: s.rjust(2, "0"), list(map(str, [self.year_to_show, self.month_to_show, i]))))) == self.selected_date
            self.day_button = Button(self.days,
                                     relief=SOLID,
                                     bg='dark grey' if self.is_selected else '#F0F0F0',
                                     fg='red' if self.is_today else 'black',
                                     text=i,
                                     font='Consolas 10 bold' if self.is_today else 'Consolas 10',
                                     padx=4,
                                     pady=4,
                                     command=lambda day=i: self.update_selected(day),
                                     height=2, width=5)
            self.day_button.grid(row=((i + cfg.week_scheme[self.month_to_show - 1]) // 7 - 1) + 1 if ((i + cfg.week_scheme[self.month_to_show - 1]) % 7 == 0) else ((i + cfg.week_scheme[self.month_to_show - 1]) // 7) + 1,
                                 column=6 if ((i + cfg.week_scheme[self.month_to_show - 1]) % 7 == 0) else ((i + cfg.week_scheme[self.month_to_show - 1]) % 7 - 1))

        for i in range(7):

            self.days.grid_columnconfigure(i, weight=1)

        self.days.grid_rowconfigure(0, weight=1)

    def update_display(self, direction):

        self.month_to_show += direction

        self.month_button['text'] = cfg.months[self.month_to_show - 1]

        self.days.destroy()
        self.load_days()

    def update_selected(self, day):

        self.parent.save_records()
        date_string = list(map(str, [self.year_to_show, self.month_to_show, day]))
        date_padded = list(map(lambda s: s.rjust(2, "0"), date_string))
        self.selected_date = '/'.join(date_padded)

        self.parent.refresh_records()

        self.days.destroy()
        self.load_days()


class Diary(LabelFrame):

    def __init__(self, parent):

        self.parent = parent
        self.records = {}

        LabelFrame.__init__(self, self.parent, bd=2)

        self.save_button = Button(self, text='Save', command=self.save_records)
        self.save_button.grid(row=0, column=0, sticky=W)

        self.calendar = Calendar(self)
        self.calendar.grid(row=1, column=0, sticky=N + E + W)

        self.panel = Panel(self)
        self.panel.load()
        self.panel.grid(row=1, column=1, sticky=N + S + E + W)

        self.load_records()

        self.refresh_records()

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

    def save_records(self):

        # TODO: save records when clicking close button
        # TODO: reorganize records when hour and/or date are edited
        # TODO: study the forbidden characters for text entry
        if self.calendar.selected_date in self.records.keys():

            self.records[self.calendar.selected_date] = []

            for child in self.panel.frame.winfo_children():
                new_text = child.text.get("1.0", "end-1c")
                new_date = child.date.get()
                new_time = child.time.get()
                new_images = child.images
                self.records[self.calendar.selected_date].append([new_date, new_time, new_text, new_images])

            with open('records.txt', 'w') as file:
                file.write('-----\n')
                for i in sorted(self.records.keys()):
                    file.write('\n')
                    for j in self.records[i]:
                        file.write('>' + ';'.join(j[:-1]) + '|' + ';'.join(j[-1]) + '\n')
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
                                text, images = entry.split('|')
                                processed_entry = text.split(';')
                                if images == '':
                                    processed_images = []
                                else:
                                    processed_images = images.split(';')
                                processed_entry.append(processed_images)
                                aux.append(processed_entry)
                        date = aux[0][0]
                        self.records[date] = aux
        except:
            open('records_new.txt', 'w').close()

    def refresh_records(self):

        self.panel.frame.destroy()
        self.panel.load()

        if self.calendar.selected_date in self.records.keys():

            for i in range(len(self.records[self.calendar.selected_date])):
                Record(self, i, self.records[self.calendar.selected_date][i])

        else:

            Record(self, position=0, content=['-', '-', 'Press the "^" button to add a Record above\nPress the "v" button to add a Record below', []])

        self.panel.conf()


class Schedule(LabelFrame):

    def __init__(self, parent):

        self.parent = parent

        LabelFrame.__init__(self, self.parent, relief=SOLID)

        self.save_button = Button(self, text='Save')
        self.save_button.grid(row=0, column=0, sticky=W)

        self.calendar = Calendar(self)
        self.calendar.grid(row=1, column=0, sticky=N + E + W)

        self.panel = Panel(self)
        self.panel.load()
        self.panel.grid(row=1, column=1, sticky=N + E + W)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
