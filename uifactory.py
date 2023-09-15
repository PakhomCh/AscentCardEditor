import customtkinter as ctk
from tkinter import ttk

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
    # CHANGE THIS ONE TO FIND ELEMENTS FROM INNER GRIDS
    def FindWidget(self, wcode):
        for itera in self.widgets:
            if itera[0] == wcode:
                return itera[1]
        return None
            

# This class is a window to be used as a parent to 
# other blocks and can be ran in a mainloop
# Window can be either Designer, Artist or Launcher type
class CoreWindow(ctk.CTk):

    def __init__(self, observer, style = 'launcher'):
        super().__init__()
        
        self.type = style
        self.__setgrid__()
        self.__setsize__()
        self.__build__()
        
        

    def __setgrid__(self):

        # Gridding this window        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def __setsize__(self):

        # Get height of a user's screen
        screenw = self.winfo_screenwidth()
        screenh = self.winfo_screenheight()

        # Set width and height of a window
        winh = screenh // 2
        winw = winh // 3 * 4

        # Set window coordinates to middle of screen
        x = (screenw - winw) // 2
        y = (screenh - winh) // 2

        self.geometry(str(winw) + 'x' + str(winh) + '+' + str(x) + '+' + str(y))
        
        # Set scaling 
        match(self.type):
            case 'artist':
                self.after_idle(lambda: self.state('zoomed'))
            case 'designer':
                self.after_idle(lambda: self.state('zoomed'))
            case 'launcher':
                pass
            
    def __build__(self):
        # This function runs a builder function specific to a window type
        match(self.type):
            case 'artist':
                self.__buildartist__()
            case 'designer':
                self.__builddesigner__()
            case 'launcher':
                self.__buildlauncher__()
        self.widgets.grid(row=0, column=0, sticky='nwse')
            
    def __buildlauncher__(self):
        self.widgets = WidgetGrid(self, (1, 1, 1), (1, 1))
        self.widgets.AddWidget(ctk.CTkLabel(self.widgets, text='Ascent Card Editor', font=('Colus', 40)), (0, 0), (1, 2))
        self.widgets.AddWidget(ctk.CTkButton(self.widgets, text='Режим дизайнера', font=('Spectral', 20)), (1, 1))
        self.widgets.AddWidget(ctk.CTkButton(self.widgets, text='Режим художника', font=('Spectral', 20)), (2, 1))

        # Adding grid for file table
        self.widgets.AddWidget(WidgetGrid(self.widgets), (1, 0), (2, 1), 'tablegrid')
        tablegrid = self.widgets.FindWidget('tablegrid')

        # Adding table of files
        table = ttk.Treeview(tablegrid, columns=('filename'), show='headings')
        table.heading('filename', text='Имя файла')
        tablegrid.AddWidget(table, (0, 0), wcode='setfiletable')

        # Adding scrollbar for table
        tablegrid.AddWidget(ctk.CTkScrollbar(tablegrid, command=table.yview), (0, 1), sticky='nse')

        # Adding table for management buttons and buttons themselves
        tablegrid.AddWidget(WidgetGrid(tablegrid, hweights=(1, 1)), (1, 0), (1, 2), 'managegrid', sticky='wse')
        managegrid = tablegrid.FindWidget('managegrid')
        self.widgets.AddWidget(ctk.CTkButton(managegrid, text='Обновить', font=('Spectral', 14)), (0, 0))
        self.widgets.AddWidget(ctk.CTkButton(managegrid, text='Создать', font=('Spectral', 14)), (0, 1))
        
