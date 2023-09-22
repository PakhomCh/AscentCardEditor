import customtkinter as ctk
import os
from tkinter import ttk, NO, END

# This file is a factory for ctk objects and widgets/components
# that can be used to simplify building UI

class WidgetGrid(ctk.CTkFrame):
    def __init__(self, master, vweights=None, hweights=None):
        super().__init__(master)

        self.master = master
        self.hweights = hweights
        self.vweights = vweights

        # Fill inner grid array with empty widget slots
        self.widgets = []

        # Setting grid weights
        self.__setgrid__()

    def __setgrid__(self):
        # Set coulum weights
        if self.hweights is not None:
            for itera in range(len(self.hweights)):
                self.columnconfigure(itera, weight=self.hweights[itera])
        else:
            self.columnconfigure(0, weight=1)
        
        # Set row weights
        if self.vweights is not None:
            for itera in range(len(self.vweights)):
                self.rowconfigure(itera, weight=self.vweights[itera])
        else:
            self.rowconfigure(0, weight=1)
        
    def AddWidget(self, widget, placement, size=(1, 1), wcode=None, sticky='nwse'):
        self.widgets.append((wcode, widget))
        widget.grid(row=placement[0], column=placement[1], rowspan=size[0], columnspan=size[1], padx=5, pady=5, sticky=sticky)
        
    # This function looks through all the widget list to find a 
    # widgetwith an exact widget code. If no widget is found, 
    # returns None
    def FindWidget(self, wcode):
        for itera in self.widgets:
            if itera[0] == wcode:
                return itera[1]
        for itera in self.widgets:
            if isinstance(itera[1], WidgetGrid):
                result = itera[1].FindWidget(wcode)
                if result is not None:
                    return result
        return None

class CustomDialog(ctk.CTkToplevel):
    def __init__(self, text, title, values):
        super().__init__()
        self.values = values
        self.text = text
        self.titles = [x[1] for x in values]
        self.result = None
        
        self.title(title)
        self.lift()  # lift window on top
        self.attributes("-topmost", True)  # stay on top
        self.protocol("WM_DELETE_WINDOW", self.__onclosing__)
        self.after(10, self.__createwidgets__)  # create widgets with slight delay, to avoid white flickering of background
        self.resizable(False, False)
        self.grab_set()  # make other windows not clickable

        
    def __createwidgets__(self):
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        weights = []
        for itera in range(2 + len(self.values)):
            weights.append(1)
        self.widgets = WidgetGrid(self, weights)
        self.widgets.grid(row=0, column=0, padx=5, pady=5, sticky='nwe')

        self.widgets.AddWidget(ctk.CTkLabel(self.widgets, text=self.text), (0, 0))
        for itera in range(len(self.values)):
            req = self.values[itera]
            match(req[0]):
                case 'text':
                    self.widgets.AddWidget(ctk.CTkEntry(self.widgets, placeholder_text=req[1]), (1 + itera, 0), wcode=req[1])
                case 'choice':
                    options = req[2]
                    self.widgets.AddWidget(ctk.CTkOptionMenu(self.widgets, values=options), (1 + itera, 0), wcode=req[1])

        self.widgets.AddWidget(ctk.CTkButton(self.widgets, text='Создать', command=self.__createevent__), (1 + len(self.values), 0))

    def __createevent__(self):
        self.result = [self.widgets.FindWidget(x).get() for x in self.titles]
        self.grab_release()
        self.destroy()

    def __onclosing__(self):
        self.grab_release()
        self.destroy()

    def Get(self):
        self.master.wait_window(self)
        return self.result
            

# This class is a window to be used as a parent to 
# other blocks and can be ran in a mainloop
# Window can be either Designer, Artist or Launcher type
class UiHandler():

    def __init__(self, master, style = 'launcher'):
        super().__init__()
        
        self.style = style
        self.master = master
        self.__build__()
            
    def __build__(self):
        # This function runs a builder function specific to a window type
        match(self.style):
            case 'artist':
                self.__buildartist__()
            case 'designer':
                self.__builddesigner__()
                self.__updatecardtable__()
            case 'launcher':
                self.__buildlauncher__()
                self.__updatesettable__()
        self.widgets.grid(row=0, column=0, sticky='nwse')

    def __changestyle__(self, style):
        if self.style == 'launcher' and self.widgets.FindWidget('setfiletable').focus() == '':
            pass
        elif self.style == 'launcher':
            table = self.widgets.FindWidget('setfiletable')
            name = table.item(table.focus())['values'][0]
            self.master.OpenSet(name)
            self.widgets.destroy()
            self.style = style
            self.__build__()
            self.master.SetScaling()
        else:
            self.widgets.destroy()
            self.style = style
            self.__build__()
            self.master.SetScaling()

            
    def __buildlauncher__(self):
        self.widgets = WidgetGrid(self.master, (1, 1, 1), (1, 1))
        self.widgets.AddWidget(ctk.CTkLabel(self.widgets, text='Ascent Card Editor', font=('Colus', 40)), (0, 0), (1, 2))
        self.widgets.AddWidget(ctk.CTkButton(self.widgets, text='Режим дизайнера', font=('Spectral', 20), command=lambda: self.__changestyle__('designer')), (1, 1))
        self.widgets.AddWidget(ctk.CTkButton(self.widgets, text='Режим художника', font=('Spectral', 20), command=lambda: self.__changestyle__('artist')), (2, 1))

        # Adding grid for file table
        self.widgets.AddWidget(WidgetGrid(self.widgets), (1, 0), (2, 1), 'tablegrid')
        tablegrid = self.widgets.FindWidget('tablegrid')

        # Adding table of files
        table = ttk.Treeview(tablegrid, columns=('filename'), show='headings')
        table.heading('#0', text = '', anchor = 'center')
        table.column('#0', width = 0, stretch = NO, anchor = 'center')
        table.heading('filename', text='Имя файла', anchor = 'center')
        table.column('filename', anchor = 'center')
        tablegrid.AddWidget(table, (0, 0), wcode='setfiletable')

        # Adding scrollbar for table
        tablegrid.AddWidget(ctk.CTkScrollbar(tablegrid, command=table.yview), (0, 1), wcode='scrollbar', sticky='nse')
        scrollbar = self.widgets.FindWidget('scrollbar')
        table.configure(yscrollcommand=scrollbar.set)

        # Adding table for management buttons and buttons themselves
        tablegrid.AddWidget(WidgetGrid(tablegrid, hweights=(1, 1)), (1, 0), (1, 2), 'managegrid', sticky='wse')
        managegrid = tablegrid.FindWidget('managegrid')
        self.widgets.AddWidget(ctk.CTkButton(managegrid, text='Обновить', font=('Spectral', 14), command=self.__updatesettable__), (0, 0))
        self.widgets.AddWidget(ctk.CTkButton(managegrid, text='Создать', font=('Spectral', 14), command=self.__createnewset__), (0, 1))
        
    def __builddesigner__(self):
        self.widgets = WidgetGrid(self.master, (5, 1), (2, 3))
        self.widgets.AddWidget(ctk.CTkLabel(self.widgets, text='Card in work', font=('Spectral', 20)), (0, 0), wcode='cardimage')
        self.widgets.AddWidget(ctk.CTkTextbox(self.widgets,font=('Spectral', 16)), (1, 0), wcode='cardtext')

        # Adding grid for card table
        self.widgets.AddWidget(WidgetGrid(self.widgets), (0, 1), wcode='tablegrid')
        tablegrid = self.widgets.FindWidget('tablegrid')

        # Adding table of files
        columns = ('id', 'cardname', 'cost', 'color', 'type', 'subtype', 'text', 'power')
        columnweights = [40, 150, 75, 75, 100, 150, 150, 40]
        table = ttk.Treeview(tablegrid, columns=columns, show='headings')

        # Set headings for table
        table.column('#0', width=0, stretch=NO)
        table.heading('#0', text='', anchor='center')
        table.heading('id', text='№')
        table.column('id', anchor='center')
        table.heading('cardname', text='Название')
        table.heading('cost', text='Стоимость')
        table.column('cost', anchor='center')
        table.heading('color', text='Цвет')
        table.column('color', anchor='center')
        table.heading('type', text='Тип')
        table.heading('subtype', text='Подтип')
        table.heading('text', text='Текст')
        table.heading('power', text='Сила')
        table.column('power', anchor='center')
        for itera in range(len(columns)):
            table.column(columns[itera], width=columnweights[itera])
        tablegrid.AddWidget(table, (0, 0), wcode='cardtable')
        table.bind_all("<<TreeviewSelect>>", lambda e: self.__loadcard__())

        # Adding scrollbar for table
        tablegrid.AddWidget(ctk.CTkScrollbar(tablegrid, command=table.yview), (0, 1), wcode='scrollbar', sticky='nse')
        scrollbar = self.widgets.FindWidget('scrollbar')
        table.configure(yscrollcommand=scrollbar.set)

        # Adding grid for all the input boxes
        self.widgets.AddWidget(WidgetGrid(self.widgets, (1, 1, 1), (1, 1)), (1, 1), wcode='inputsgrid')
        inputsgrid = self.widgets.FindWidget('inputsgrid')
        self.widgets.AddWidget(ctk.CTkEntry(inputsgrid, placeholder_text='Имя карты', font=('Spectral', 16)), (0, 0), wcode='cardname')
        self.widgets.AddWidget(ctk.CTkEntry(inputsgrid, placeholder_text='Стоимость карты', font=('Spectral', 16)), (0, 1), wcode='cardcost')
        self.widgets.AddWidget(ctk.CTkEntry(inputsgrid, placeholder_text='Тип карты', font=('Spectral', 16)), (1, 0), wcode='cardtype')
        self.widgets.AddWidget(ctk.CTkEntry(inputsgrid, placeholder_text='Цвет карты', font=('Spectral', 16)), (1, 1), wcode='cardcolor')
        self.widgets.AddWidget(ctk.CTkEntry(inputsgrid, placeholder_text='Подтип карты', font=('Spectral', 16)), (2, 0), wcode='cardsubtype')
        self.widgets.AddWidget(ctk.CTkEntry(inputsgrid, placeholder_text='Сила карты (или X)', font=('Spectral', 16)), (2, 1), wcode='cardpower')
    
    # Used in Designer mode to fill Entry boxes with card values
    def __loadcard__(self):
        table = self.widgets.FindWidget('cardtable')
        values = table.item(table.focus())['values']

        cardname = self.widgets.FindWidget('cardname')
        cardname.delete(0, END)
        cardname.insert(END, values[1])
        
        cardcost = self.widgets.FindWidget('cardcost')
        cardcost.delete(0, END)
        cardcost.insert(END, values[2])

        cardtype = self.widgets.FindWidget('cardtype')
        cardtype.delete(0, END)
        cardtype.insert(END, values[4])

        cardcolor = self.widgets.FindWidget('cardcolor')
        cardcolor.delete(0, END)
        cardcolor.insert(END, values[3])

        cardsubtype = self.widgets.FindWidget('cardsubtype')
        cardsubtype.delete(0, END)
        cardsubtype.insert(END, values[5])

        cardpower = self.widgets.FindWidget('cardpower')
        cardpower.delete(0, END)
        cardpower.insert(END, values[7])

    # Used in Launcher mode to update table of all set files
    def __updatesettable__(self):
        tabledata = [x.split('.ace-set')[0] for x in os.listdir('.\sets') if '.ace-set' in x]
        table = self.widgets.FindWidget('setfiletable')
        table.delete(*table.get_children())
        
        for itera in range(len(tabledata)):
            table.insert(parent='', index='end', iid=itera, text='', values=tabledata[itera])
            
    def __createnewset__(self):
        request = (('text', 'Название сета'), ('text', 'Код сета'), ('choice', 'Тип сета', ('Default (50 + 5)', 'Core (250 + 10)', 'Base (36)', 'Empty', 'Custom')), ('text', 'Релиз: *-**'))
        data = CustomDialog('Заполните информацию о сете', 'Новый сет', request).Get()
        if data is not None:
            data[2] = data[2].split()[0]
            self.master.AddSet(data)
        self.__updatesettable__()

    # Used in Designer mode to update table of all cards within set
    def __updatecardtable__(self):
        table = self.widgets.FindWidget('cardtable')
        table.delete(*table.get_children())
        data = self.master.GetSetCards()
        for itera in range(len(data)):
            table.insert(parent='', index='end', iid=itera, text='', values=data[itera])

    def FindWidget(self, wcode):
        return self.widgets.FindWidget(wcode)

    def Style(self):
        return self.style
    