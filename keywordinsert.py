from tkinter import Toplevel, LabelFrame, Label, Entry, Button
from tkinter import N, S, W, E, END
from tkinter.ttk import Combobox
from PIL import Image
from PIL.ImageTk import PhotoImage

class KeywordInsert():

    def __init__(self, master, color):

        self.master = master
        self.CT = color
        self.__window = Toplevel()
        self.__create_window()
        self.__create_widgets()
        
    def close(self):

        self.__window.destroy()

    def __create_window(self):

        self.__window.title('Вставка ключевых слов')
        x = 70
        self.__window.minsize(4 * x, 1 * x)

        self.__window.rowconfigure(0, weight = 1)
        self.__window.rowconfigure(1, weight = 3)

        self.__window.columnconfigure(0, weight = 1)

    def __create_widgets(self):

        self.__text_frame = LabelFrame(self.__window)
        self.__text_frame.rowconfigure(0, weight = 1)
        self.__text_frame.columnconfigure(0, weight = 1)
        self.__text_frame.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = N + W + S + E)

        self.__value_frame = LabelFrame(self.__window)
        self.__value_frame.rowconfigure(0, weight = 1)
        self.__value_frame.rowconfigure(1, weight = 1)
        self.__value_frame.rowconfigure(2, weight = 1)
        self.__value_frame.columnconfigure(0, weight = 1)
        self.__value_frame.grid(row = 1, column = 0, padx = 10, pady = 10, sticky = N + W + S + E)

        self.__set_text_frame()
        self.__set_value_frame()

        color = self.CT
        cm = self.master.color_themes['colors'][color][0]
        cs = self.master.color_themes['colors'][color][1]
        ce = self.master.color_themes['colors'][color][2]
        ct = self.master.color_themes['colors'][color][3]

        self.__window.config(bg = cm)

        frame_list = [self.__text_frame, 
                      self.__value_frame]
        for i in frame_list:
            i.config(bg = cs)
            i.config(fg = ct)

        widget_list = [self.__keyword_combo,
                       self.__update_button,
                       self.__insert_button]
        for i in widget_list:
            try:
                i.config(bg = ce)
            except:
                pass
            try:
                i.config(fg = ct)
            except:
                pass

        self.__text_label.config(fg = ct)
        self.__text_label.config(bg = cs)

    def __set_text_frame(self):

        self.__text_label = Label(self.__text_frame, font = self.master.fonts['mainfont'], text = 'Выберите ключевое слово из предложенных ниже.')
        self.__text_label.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = N + W + S + E)

    def __set_value_frame(self):
        
        kw = self.master.ingame['keywords']['words']

        self.__keyword_combo = Combobox(self.__value_frame, values = kw)
        self.__keyword_combo.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = N + W + S + E)

        self.__update_button = Button(self.__value_frame, text = 'Отобразить текст', command = self.__update_text)
        self.__update_button.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = N + W + S + E)

        self.__insert_button = Button(self.__value_frame, text = 'Добавить на карту', command = self.__insert_text)
        self.__insert_button.grid(row = 2, column = 0, padx = 5, pady = 5, sticky = N + W + S + E)

    def __update_text(self):

        kw = self.master.ingame['keywords']['words']

        keyword = kw[self.__keyword_combo.current()]
        ruletext = self.master.ingame['keywords']['rules'][keyword]
        self.__text_label['text'] = ruletext

    def __insert_text(self):

        kw = self.master.ingame['keywords']['words']

        keyword = kw[self.__keyword_combo.current()]
        ruletext = self.master.ingame['keywords']['rules'][keyword]
        self.master.window.collect_text(ruletext)

pass