from tkinter import Menu, END

class MenuHandler():
    def __init__(self, master, style='launcher'):
        self.master = master
        self.style = style
        if style != 'launcher':
            self.__build__()
        self.menu = Menu(self.master)
    
    def __build__(self):
        self.menu = Menu(self.master)
        self.menubar = {}

        self.menubar['editor'] = Menu(self.menu, tearoff=0)
        self.menubar['editor'].add_command(label='К лаунчеру', underline=0, command=self.blank)
        self.menubar['editor'].add_separator()
        self.menubar['editor'].add_command(label='Смена режима', underline=0, command=self.blank)
        self.menu.add_cascade(label='Редактор', underline=0, menu=self.menubar['editor'])

        self.menubar['set'] = Menu(self.menu, tearoff=0)
        self.menubar['set'].add_command(label='Сохранить', underline=0, command=lambda: self.master.SaveSet())
        self.menubar['set'].add_command(label='Загрузить', underline=0, command=self.blank)
        self.menubar['export'] = Menu(self.menubar['set'], tearoff=0)
        self.menubar['export'].add_command(label='В JSON', underline=0, command=self.blank)
        self.menubar['export'].add_command(label='Целиком', underline=0, command=self.blank)
        self.menubar['set'].add_cascade(label='Экспортировать', underline=0, menu=self.menubar['export'])
        self.menubar['set'].add_separator()
        self.menubar['goto'] = Menu(self.menubar['set'], tearoff=0)
        self.menubar['goto'].add_command(label='К картам', underline=0, command=self.blank)
        self.menubar['goto'].add_command(label='К токенам', underline=0, command=self.blank)
        self.menubar['set'].add_cascade(label='Перейти', underline=0, menu=self.menubar['goto'])
        self.menu.add_cascade(label='Издание', underline=0, menu=self.menubar['set'])

        self.menubar['card'] = Menu(self.menu, tearoff=0)
        self.menubar['card'].add_command(label='Добавить', underline=0, command=self.blank)
        self.menubar['card'].add_command(label='Удалить', underline=0, command=self.blank)
        self.menubar['card'].add_separator()
        self.menubar['card'].add_command(label='Ключевые слова', underline=0, command=self.blank)
        self.menu.add_cascade(label='Карта', underline=0, menu=self.menubar['card'])

        self.menubar['about'] = Menu(self.menu, tearoff=0)
        self.menubar['about'].add_command(label='Памятка', underline=0, command=self.blank)
        self.menu.add_cascade(label='Справка', underline=0, menu=self.menubar['about'])

        self.menubar['options'] = Menu(self.menu, tearoff=0)
        self.menubar['options'].add_command(label='Добавить код доступа', underline=0, command=self.blank)
        self.menu.add_cascade(label='Параметры', underline=0, menu=self.menubar['options'])

        self.master.config(menu=self.menu)
        
    def blank(self):
        pass

    def ChangeStyle(self, style):
        self.menu.delete(0, END)
        self.style = style
        if style != 'launcher':
            self.__build__()
    
