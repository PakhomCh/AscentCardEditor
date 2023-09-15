import encodings
import os
from os import remove
from tkinter import Button, Entry, Label, Scrollbar, Tk, Menu, LabelFrame
from tkinter import N, S, W, E, END
from tkinter.constants import INSERT, NO
from tkinter.ttk import Combobox, Treeview
from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog import askopenfilename
from PIL import Image
from PIL.ImageTk import PhotoImage
from sys import exit
from io import BytesIO
from imagecut import ImageCut
from keywordinsert import KeywordInsert
from card import Card

class Window():

    def __init__ (self, master = None):

        self.master = master
        self.__image = Image.open('data/default.png')
        self.__window = Tk()
        self.__create_window()
        self.__create_menu()
        self.__create_frames()
        self.__clear()

    def run(self):

        self.__window.mainloop()

    def close(self):

        try:
            self.__imagecut.close()
        except:
            pass
        try:
            self.__keywordinsert.close()
        except:
            pass
        self.__window.destroy()
    
    def collect_image(self, image):

        self.__image = image

    def collect_text(self, text):

        self.__text_text.insert(INSERT, text + '\n')

    def __create_window(self):

        # self.__window.attributes('-fullscreen', True)
        self.__window.title('Восхождение: Редактор Карт')
        self.__window.iconbitmap('icon.ico')
        x = 250
        self.__window.minsize(5 * x, 3 * x)

        self.__window.rowconfigure(0, weight = 2)
        self.__window.rowconfigure(1, weight = 1)

        self.__window.columnconfigure(0, weight = 1)
        self.__window.columnconfigure(1, weight = 5)

    def __create_menu(self):

        self.__menubar = Menu(self.__window)
        
        self.__file_menu = Menu(self.__menubar, tearoff = 0)
        # self.__file_menu.add_command(label = 'Открыть...', underline = 1, accelerator = HK_OPEN, command = self.__window.destroy)
        # self.__window.bind_all(HK_OPEN_BIND, lambda e: <open new file>)
        self.__file_menu.add_command(label = 'Открыть готовые карты', underline = 0, command = self.__open_directory)
        self.__file_menu.add_command(label = 'Выход', underline = 1, accelerator = self.master.hotkeys['exit']['b'], command = exit)
        self.__window.bind_all(self.master.hotkeys['exit']['c'], lambda e: self.master.exit())
        self.__menubar.add_cascade(label = 'Файл', underline = 0, menu = self.__file_menu)

        self.__set_menu = Menu(self.__menubar, tearoff = 0)
        self.__set_menu.add_command(label = 'Экспортировать таблицу', underline = 1, command = self.__export_table)
        self.__set_menu.add_command(label = 'Экспортировать издание', underline = 1, command = self.__export_images)
        self.__menubar.add_cascade(label = 'Издание', underline = 0, menu = self.__set_menu)
        
        self.__edit_menu = Menu(self.__menubar, tearoff = 0)
        self.__edit_menu.add_command(label = 'Ключевые слова...', underline = 0, command = self.__open_keywordinsert)
        self.__edit_menu.add_command(label = 'Загрузить карту', underline = 1, accelerator = self.master.hotkeys['edit_card']['b'], command = self.__load_card)
        self.__window.bind_all(self.master.hotkeys['edit_card']['c'], lambda e: self.__load_card())
        self.__edit_menu.add_command(label = 'Новая карта', underline = 1, accelerator = self.master.hotkeys['clear_card']['b'], command = self.__clear)
        self.__window.bind_all(self.master.hotkeys['clear_card']['c'], lambda e: self.__clear())
        self.__edit_menu.add_command(label = 'Удалить карту', underline = 1, accelerator = self.master.hotkeys['delete_card']['b'], command = self.__delete_card)
        self.__window.bind_all(self.master.hotkeys['delete_card']['c'], lambda e: self.__delete_card())
        self.__menubar.add_cascade(label = 'Карта', underline = 0, menu = self.__edit_menu)
        
        self.__about_menu = Menu(self.__menubar, tearoff = 0)
        # self.__about_menu.add_command()
        self.__menubar.add_cascade(label = 'Справка', underline = 0, menu = self.__about_menu)

        self.__theme_menu = Menu(self.__menubar, tearoff = 0)
        self.__theme_menu.add_command(label = 'Стандартная', underline = 0, command = lambda: self.__change_theme('Стандартная тема'))
        self.__theme_menu.add_command(label = 'Фиолетовая', underline = 0, command = lambda: self.__change_theme('Фиолетовая тема'))
        self.__theme_menu.add_command(label = 'Голубая', underline = 0, command = lambda: self.__change_theme('Голубая тема'))
        self.__theme_menu.add_command(label = 'Оливковая', underline = 0, command = lambda: self.__change_theme('Оливковая тема'))
        self.__menubar.add_cascade(label = 'Тема', underline = 0, menu = self.__theme_menu)

        self.__window['menu'] = self.__menubar

    def __create_frames(self):

        rows = 5

        self.__value_frame = LabelFrame(self.__window, background = '#a0a0a0')
        for i in range(rows):
            self.__value_frame.rowconfigure(i, weight = 1)
        self.__value_frame.columnconfigure(0, weight = 1)
        self.__value_frame.columnconfigure(1, weight = 1)
        self.__value_frame.columnconfigure(2, weight = 3)
        self.__value_frame.grid(row = 1, column = 0, columnspan = 2, padx = 10, pady = 10, sticky = N + W + S + E)

        self.__image_frame = LabelFrame(self.__window, background = '#a0a0a0')
        self.__image_frame.rowconfigure(0, weight = 1)
        self.__image_frame.columnconfigure(0, weight = 1)
        self.__image_frame.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = N + W + S + E)

        self.__table_frame = LabelFrame(self.__window, background = '#a0a0a0')
        self.__table_frame.rowconfigure(0, weight = 1)
        self.__table_frame.columnconfigure(0, weight = 1)
        self.__table_frame.grid(row = 0, column = 1, padx = 10, pady = 10, sticky = N + W + S + E)

        self.__set_value_frame(rows)
        self.__set_image_frame()
        self.__set_table_frame()

        self.__change_theme('Стандартная тема')

    def __set_value_frame(self, rows):

        # Характеристики карты: Название

        self.__name_frame = LabelFrame(self.__value_frame, background = '#d0d0d0', text = 'Название карты')
        self.__name_frame.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = N + W + S + E)
        self.__name_frame.rowconfigure(0, weight = 1)
        self.__name_frame.columnconfigure(0, weight = 1)

        self.__name_entry = Entry(self.__name_frame, font = self.master.fonts['mainfont'])
        self.__name_entry.bind("<FocusOut>", lambda x: print('Focus Lost'))
        self.__name_entry.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = N + W + S + E)

        # Характеристики карты: Стоимость

        self.__cost_frame = LabelFrame(self.__value_frame, background = '#d0d0d0', text = 'Стоимость карты')
        self.__cost_frame.grid(row = 0, column = 1, padx = 5, pady = 5, sticky = N + W + S + E)
        self.__cost_frame.rowconfigure(0, weight = 1)
        self.__cost_frame.columnconfigure(0, weight = 1)

        self.__cost_entry = Entry(self.__cost_frame, font = self.master.fonts['mainfont'])
        self.__cost_entry.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = N + W + S + E)

        # Характеристики карты: Тип карты

        self.__type_frame = LabelFrame(self.__value_frame, background = '#d0d0d0', text = 'Тип карты')
        self.__type_frame.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = N + W + S + E)
        self.__type_frame.rowconfigure(0, weight = 1)
        self.__type_frame.columnconfigure(0, weight = 1)

        self.__type_combo = Combobox(self.__type_frame, values = self.master.ingame['cardtypes'], font = self.master.fonts['mainfont'])
        self.__type_combo.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = N + W + S + E)
        self.__type_combo.current(4)

        # Характеристики карты: Подтип карты

        self.__subtype_frame = LabelFrame(self.__value_frame, background = '#d0d0d0', text = 'Подтип карты')
        self.__subtype_frame.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = N + W + S + E)
        self.__subtype_frame.rowconfigure(0, weight = 1)
        self.__subtype_frame.columnconfigure(0, weight = 1)

        self.__subtype_combo = Combobox(self.__subtype_frame, values = self.master.ingame['cardsubtypes'], font = self.master.fonts['mainfont'])
        self.__subtype_combo.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = N + W + S + E)
        self.__subtype_combo.current(0)
        

        # Характеристики карты: Цвет

        self.__color_frame = LabelFrame(self.__value_frame, background = '#d0d0d0', text = 'Цвет карты')
        self.__color_frame.grid(row = 2, column = 0, padx = 5, pady = 5, sticky = N + W + S + E)
        self.__color_frame.rowconfigure(0, weight = 1)
        self.__color_frame.columnconfigure(0, weight = 1)

        self.__color_combo = Combobox(self.__color_frame, values = self.master.ingame['colors'], font = self.master.fonts['mainfont'])
        self.__color_combo.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = N + W + S + E)
        self.__color_combo.current(4)

        # Характеристики карты: Сила

        self.__power_frame = LabelFrame(self.__value_frame, background = '#d0d0d0', text = 'Сила карты')
        self.__power_frame.grid(row = 2, column = 1, padx = 5, pady = 5, sticky = N + W + S + E)
        self.__power_frame.rowconfigure(0, weight = 1)
        self.__power_frame.columnconfigure(0, weight = 1)

        self.__power_entry = Entry(self.__power_frame, font = self.master.fonts['mainfont'])
        self.__power_entry.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = N + W + S + E)

        # Характеристики карты: Художник

        self.__artist_frame = LabelFrame(self.__value_frame, background = '#d0d0d0', text = 'Художник')
        self.__artist_frame.grid(row = 3, column = 0, padx = 5, pady = 5, sticky = N + W + S + E)
        self.__artist_frame.rowconfigure(0, weight = 1)
        self.__artist_frame.columnconfigure(0, weight = 1)

        self.__artist_entry = Entry(self.__artist_frame, font = self.master.fonts['mainfont'])
        self.__artist_entry.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = N + W + S + E)

        # Характеристики карты: Изображение

        self.__artwork_frame = LabelFrame(self.__value_frame, background = '#d0d0d0', text = 'Арт карты')
        self.__artwork_frame.grid(row = 3, column = 1, padx = 5, pady = 5, sticky = N + W + S + E)
        self.__artwork_frame.rowconfigure(0, weight = 1)
        self.__artwork_frame.columnconfigure(0, weight = 1)

        self.__artwork_button = Button(self.__artwork_frame, font = self.master.fonts['mainfont'], text = 'Загрузить изображение...', command = self.__open_imagecut)
        self.__artwork_button.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = N + W + S + E)

        # Характеристики карты: Текст

        self.__text_frame = LabelFrame(self.__value_frame, background = '#d0d0d0', text = 'Текст карты')
        self.__text_frame.grid(row = 0, column = 2, rowspan = rows, padx = 5, pady = 5, sticky = N + W + S + E)
        self.__text_frame.rowconfigure(0, weight = 1)
        self.__text_frame.columnconfigure(0, weight = 1)

        self.__text_text = ScrolledText(self.__text_frame, width = 10, height = 5, font = self.master.fonts['subfont'])
        self.__text_text.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = N + W + S + E)

        # Характеристики карты: Завершение

        self.__finish_frame = LabelFrame(self.__value_frame, background = '#d0d0d0', text = 'Завершение работы')
        self.__finish_frame.grid(row = 4, column = 0, columnspan = 2, padx = 5, pady = 5, sticky = N + W + S + E)
        self.__finish_frame.rowconfigure(0, weight = 1)
        self.__finish_frame.columnconfigure(0, weight = 1)

        self.__finish_button = Button(self.__finish_frame, font = self.master.fonts['mainfont'], text = 'Обновить и сохранить карту', command = self.__save_card)
        self.__finish_button.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = N + W + S + E)

    def __set_image_frame(self):
        
        x = 60
        self.__image_disp = PhotoImage(Image.open('data/FrameW.png').resize((5 * x, 7 * x), Image.ANTIALIAS))
        self.__image_label = Label(self.__image_frame, image = self.__image_disp)
        self.__image_label.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = N + W + S + E)

    def __set_table_frame(self):

        self.__scroll_bar = Scrollbar(self.__table_frame)
        self.__scroll_bar.grid(row = 0, column = 1, sticky = N + S)

        self.__table = Treeview(self.__table_frame, columns = self.master.columns['names'])

        self.__scroll_bar.config(command = self.__table.yview)

        self.__table.column('#0', width = 0, stretch = NO)
        self.__table.heading('#0', text = '', anchor = 'center')

        for i in self.master.columns['names']:

            self.__table.column(i, width = self.master.columns['width'][i], anchor = 'center')
            self.__table.heading(i, text = i, anchor = 'center')

        self.__table.grid(row = 0, column = 0, sticky = N + W + S + E)
        self.__update_table()
        self.__table.bind_all("<<TreeviewSelect>>", lambda e: self.__load_card())

    def __update_table(self):

        self.__table.delete(*self.__table.get_children())

        table = self.master.set_access.get_table()

        for i in range(len(table)):

            temp = [*table[i]]
            temp = [temp[0]] + temp[2:]

            self.__table.insert(parent = '', index = 'end', iid = i, text = '', values = temp)

    def __change_theme(self, color):

        self.CT = color
        
        cm = self.master.color_themes['colors'][color][0]
        cs = self.master.color_themes['colors'][color][1]
        ce = self.master.color_themes['colors'][color][2]
        ct = self.master.color_themes['colors'][color][3]
        
        self.__window.config(bg = cm)

        frame_list = [self.__value_frame, 
                      self.__table_frame, 
                      self.__image_frame,
                      self.__name_frame,
                      self.__cost_frame,
                      self.__type_frame,
                      self.__subtype_frame,
                      self.__color_frame,
                      self.__power_frame,
                      self.__artist_frame,
                      self.__artwork_frame,
                      self.__finish_frame,
                      self.__text_frame]

        for i in frame_list:
            try:
                i.config(bg = cs)
            except:
                pass
            try:
                i.config(fg = ct)
            except:
                pass
            try:
                i.config(relief = 'flat')
            except:
                pass
            

        widget_list = [self.__name_entry,
                      self.__cost_entry,
                      self.__power_entry,
                      self.__artist_entry,
                      self.__artwork_button,
                      self.__finish_button,
                      self.__text_text]
        for i in widget_list:
            i.config(bg = ce)
            i.config(fg = ct)

        self.__image_label.config(bg = cs)

    def __open_directory(self):

        os.startfile(os.path.realpath('results'))

    def __open_imagecut(self):

        filename = askopenfilename(title = 'Выберите изображение для карты', filetypes = ((' Image files', '*.jpg'), (' Image files', '*.png')))

        if filename != '':

            print('IMAGE UPLOADED')

            image = Image.open(filename)

            self.__imagecut = ImageCut(self.master, self.CT, image)

    def __save_card(self):

        card = Card(self.master, self.__image, self.__color_combo.current(), self.__cost_entry.get(), self.__type_combo.current(), self.__subtype_combo.current(), self.__name_entry.get(), self.__artist_entry.get(), self.__power_entry.get(), self.__text_text.get('1.0', END)[0:-1])

        self.__update_card()
        self.master.set_access.add_card(card)
        self.__update_table()
        card.save_paper()
        card.save_web()

    def __load_card(self):

        if self.__table.item(self.__table.focus())['values'] != '':

            self.__clear()

            card_id = self.__table.item(self.__table.focus())['values'][0]

            values = self.master.set_access.get_card_values(card_id)

            self.__name_entry.insert(END, values[2])
            self.__cost_entry.insert(END, values[3])
            self.__power_entry.insert(END, values[8])
            self.__artist_entry.insert(END, values[9])
            self.__text_text.insert(INSERT, values[7])

            self.__type_combo.current(self.master.ingame['cardtypes'].index(values[5]))
            self.__subtype_combo.current(self.master.ingame['cardsubtypes'].index(values[6]))
            self.__color_combo.current(self.master.ingame['colors'].index(values[4]))

            # with open('temp/temp.png', 'wb') as file:
                # file.write(values[1])
            self.__image = Image.open(BytesIO(values[1]))

            self.__update_card()
        
    def __delete_card(self):

        if self.__table.item(self.__table.focus())['values'] != '':
            card_id = self.__table.item(self.__table.focus())['values'][0]
            self.master.set_access.delete_card(card_id)
            self.__update_table()

    def __update_card(self, card = None):

        if card == None:
            card = Card(self.master, self.__image, self.__color_combo.current(), self.__cost_entry.get(), self.__type_combo.current(), self.__subtype_combo.current(), self.__name_entry.get(), self.__artist_entry.get(), self.__power_entry.get(), self.__text_text.get('1.0', END)[0:-1])

        x = 60
        self.__image_disp = PhotoImage(card.build().crop((15, 15, 759, 1054)).resize((5 * x, 7 * x), Image.ANTIALIAS))
        self.__image_label["image"] = self.__image_disp

    def __clear(self):

        self.__name_entry.delete(0, END)
        self.__cost_entry.delete(0, END)
        self.__power_entry.delete(0, END)
        self.__artist_entry.delete(0, END)
        self.__text_text.delete('1.0', END)
        self.__type_combo.current(0)
        self.__subtype_combo.current(0)
        self.__color_combo.current(0)

        x = 60
        self.__image_disp = PhotoImage(Image.open('data/FrameW.png').resize((5 * x, 7 * x), Image.ANTIALIAS))
        self.__image_label["image"] = self.__image_disp

    def __open_keywordinsert(self):

        self.__keywordinsert = KeywordInsert(self.master, self.CT)

    def __export_table(self):
        
        table = self.master.set_access.get_data()
        setfile = open('sets/01.Ascent.xml', 'w+', encoding = 'utf-8')

        # setfile.write('<!--CREATED AUTOMATICALLY WITH ASCENT SET EDITOR, COPYRIGHT KONTINUUM LLC-->\n<?xml version="1.0" encoding="UTF-8"?>\n<cockatrice_carddatabase version="4">\n\t<sets>\n\t\t<set>\n\t\t\t<name>ACS</name>\n\t\t\t<longname>Kontinuum: Ascent</longname>\n\t\t\t<settype>Custom</settype>\n\t\t\t<releasedate></releasedate>\n\t\t</set>\n\t</sets>\n\t<cards>\n')
        setfile.write('<?xml version="1.0" encoding="UTF-8"?>\n<cockatrice_carddatabase version="4">\n\t<sets>\n\t\t<set>\n\t\t\t<name>ACS</name>\n\t\t\t<longname>Kontinuum: Ascent</longname>\n\t\t\t<settype>Custom</settype>\n\t\t\t<releasedate></releasedate>\n\t\t</set>\n\t</sets>\n\t<cards>\n')
        for i in table:
            text = i[5]
            while '-- ' in text or '*' in text or '_' in text or '!' in text:
                text = text.replace('-- ', '— ')
                text = text.replace('*', '')
                text = text.replace('_', '')
                text = text.replace('!', '')
            setfile.write('\t\t<card>\n\t\t\t<name>' + i[0] + '</name>\n\t\t\t<text>' + text + '</text>\n\t\t\t<prop>\n\t\t\t\t<manacost>' + str(i[1]) + '</manacost>\n\t\t\t\t<pt>' + str(i[6]) + '</pt>\n\t\t\t\t<maintype>' + i[3] + '</maintype>\n\t\t\t\t<type>' + i[3] + '</type>\n\t\t\t\t<colors>' + i[2] + '</colors>\n\t\t\t</prop>\n\t\t\t<tablerow>3</tablerow>\n\t\t\t<set>ACS</set>\n\t\t</card>\n')
        setfile.write('\t</cards>\n</cockatrice_carddatabase>')
        print('DATA EXPORTED')
        setfile.close()

    def __export_images(self):

        total = self.master.set_access.size()
        count = 0

        table = self.master.set_access.get_table()
        for values in table:
            with open('temp/temp.png', 'wb') as file:
                file.write(values[1])
            image = Image.open('temp/temp.png')
            color = self.master.ingame['colors'].index(values[4])
            cost = values[3]
            cardtype = self.master.ingame['cardtypes'].index(values[5])
            cardsubtype = self.master.ingame['cardsubtypes'].index(values[6])
            name = values[2]
            artist = values[9]
            power = values[8]
            text = values[7]

            card = Card(self.master, image, color, cost, cardtype, cardsubtype, name, artist, power, text)

            card.save_web()
            card.save_paper()

            count += 1
            print('[' + str(count) + ' / ' + str(total) + ']: EXPORTED "' + name + '"' )

pass