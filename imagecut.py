from tkinter import Toplevel, LabelFrame, Label, Entry, Button
from tkinter import N, S, W, E, END
from PIL import Image
from PIL.ImageTk import PhotoImage

class ImageCut():

    def __init__(self, master, color, image):

        self.master = master
        self.CT = color
        self.original_image = image
        self.__window = Toplevel()
        self.__create_window()
        # self.__create_menu()
        self.__create_widgets()
        self.__update_image()
        
    def close(self):

        self.__window.destroy()

    def __create_window(self):

        self.__window.title('Обрезка изображения')
        x = 70
        self.__window.minsize(5 * x, 9 * x)

        self.__window.rowconfigure(0, weight = 7)
        self.__window.rowconfigure(1, weight = 2)

        self.__window.columnconfigure(0, weight = 1)

    def __create_widgets(self):

        self.__image_frame = LabelFrame(self.__window, background = '#a0a0a0')
        self.__image_frame.rowconfigure(0, weight = 1)
        self.__image_frame.columnconfigure(0, weight = 1)
        self.__image_frame.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = N + W + S + E)

        self.__value_frame = LabelFrame(self.__window, background = '#a0a0a0')
        self.__value_frame.rowconfigure(0, weight = 1)
        self.__value_frame.rowconfigure(1, weight = 1)
        self.__value_frame.columnconfigure(0, weight = 1)
        self.__value_frame.columnconfigure(1, weight = 1)
        self.__value_frame.columnconfigure(2, weight = 1)
        self.__value_frame.grid(row = 1, column = 0, padx = 10, pady = 10, sticky = N + W + S + E)

        self.__set_value_frame()
        self.__set_image_frame()

        color = self.CT
        cm = self.master.color_themes['colors'][color][0]
        cs = self.master.color_themes['colors'][color][1]
        ce = self.master.color_themes['colors'][color][2]
        ct = self.master.color_themes['colors'][color][3]

        self.__window.config(bg = cm)

        frame_list = [self.__image_frame,
                      self.__value_frame,
                      self.__xs_frame,
                      self.__ys_frame,
                      self.__scale_frame,
                      self.__update_frame,
                      self.__finish_frame]
        for i in frame_list:
            i.config(bg = cs)
            i.config(fg = ct)

        widget_list = [self.__xs_entry,
                       self.__ys_entry,
                       self.__scale_entry,
                       self.__update_button,
                       self.__finish_button]
        for i in widget_list:
            i.config(bg = ce)
            i.config(fg = ct)

        self.__image_label.config(bg = cs)

    def __set_value_frame(self):

        # Характеристики изображения: Сдвиг по х

        self.__xs_frame = LabelFrame(self.__value_frame, background = '#d0d0d0', text = 'Сдвиг по х')
        self.__xs_frame.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = N + W + S + E)
        self.__xs_frame.rowconfigure(0, weight = 1)
        self.__xs_frame.columnconfigure(0, weight = 1)

        self.__xs_entry = Entry(self.__xs_frame, font = self.master.fonts['mainfont'])
        self.__xs_entry.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = N + W + S + E)
        self.__xs_entry.insert(END, '0')

        # Характеристики изображения: Сдвиг по y

        self.__ys_frame = LabelFrame(self.__value_frame, background = '#d0d0d0', text = 'Сдвиг по y')
        self.__ys_frame.grid(row = 0, column = 1, padx = 5, pady = 5, sticky = N + W + S + E)
        self.__ys_frame.rowconfigure(0, weight = 1)
        self.__ys_frame.columnconfigure(0, weight = 1)

        self.__ys_entry = Entry(self.__ys_frame, font = self.master.fonts['mainfont'])
        self.__ys_entry.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = N + W + S + E)
        self.__ys_entry.insert(END, '0')

        # Характеристики изображения: Масштабирование

        self.__scale_frame = LabelFrame(self.__value_frame, background = '#d0d0d0', text = 'Масштабирование, в %')
        self.__scale_frame.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = N + W + S + E)
        self.__scale_frame.rowconfigure(0, weight = 1)
        self.__scale_frame.columnconfigure(0, weight = 1)

        self.__scale_entry = Entry(self.__scale_frame, font = self.master.fonts['mainfont'])
        self.__scale_entry.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = N + W + S + E)
        self.__scale_entry.insert(END, '100')

        # Характеристики изображения: Обновление

        self.__update_frame = LabelFrame(self.__value_frame, background = '#d0d0d0', text = 'Обрезка')
        self.__update_frame.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = N + W + S + E)
        self.__update_frame.rowconfigure(0, weight = 1)
        self.__update_frame.columnconfigure(0, weight = 1)

        self.__update_button = Button(self.__update_frame, font = self.master.fonts['mainfont'], text = 'Обновить', command = self.__update_image)
        self.__update_button.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = N + W + S + E)

        # Характеристики изображения: Сохранение

        self.__finish_frame = LabelFrame(self.__value_frame, background = '#d0d0d0', text = 'Завершение')
        self.__finish_frame.grid(row = 2, column = 0, columnspan = 2, padx = 5, pady = 5, sticky = N + W + S + E)
        self.__finish_frame.rowconfigure(0, weight = 1)
        self.__finish_frame.columnconfigure(0, weight = 1)

        self.__finish_button = Button(self.__finish_frame, font = self.master.fonts['mainfont'], text = 'Применить', command = self.close)
        self.__finish_button.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = N + W + S + E)

    def __set_image_frame(self):
        
        self.__image_label = Label(self.__image_frame)
        self.__image_label.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = N + W + S + E)

    def __update_image(self):

        x = 60

        x_shift = int(self.__xs_entry.get())
        y_shift = int(self.__ys_entry.get())

        scale = int(self.__scale_entry.get())

        pic = self.original_image.copy()
        frame = Image.open('data/FrameN.png')
        mask = Image.open('data/FrameMask.png').convert('L')

        h = (pic.height) * scale // 100
        w = (pic.width) * scale // 100

        pic = pic.resize((w, h), Image.ANTIALIAS)

        pic = pic.crop((x_shift, y_shift, x_shift + 774, y_shift + 1069))

        self.master.window.collect_image(pic.copy())

        pic.paste(frame, (15, 15), mask)

        self.image = PhotoImage(pic.resize((5 * x, 7 * x), Image.ANTIALIAS))

        self.__image_label['image'] = self.image

pass