import customtkinter as ctk
from uihandler import UiHandler
from xmlhandler import SetHandler

class AscentCardEditor(ctk.CTk):

    def __init__(self):
        super().__init__()

        # Legacy code
        # self.dat_access = DatAccess()
        # self.hotkeys = self.dat_access.hotkeys()
        # self.fonts = self.dat_access.fonts()
        # self.ingame = self.dat_access.ingame()
        # self.columns = self.dat_access.columns()
        # self.set_access = SetAccess(master = self)
        # self.color_themes = self.dat_access.color_themes()
        # self.window = Window(master = self)
        
        self.uihandler = UiHandler(self)
        self.sethandler = SetHandler()
        self.__setsize__()
        self.SetScaling()

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
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def AddSet(self, data):
        self.sethandler.New(*data)
        self.sethandler.Save()
        self.sethandler.Drop()

    def OpenSet(self, name):
        self.sethandler.Load(name)

    def GetSetCards(self):
        return self.sethandler.CardTable()

    def SetScaling(self):
        match(self.uihandler.Style()):
            case 'artist':
                self.after_idle(lambda: self.state('zoomed'))
            case 'designer':
                self.after_idle(lambda: self.state('zoomed'))
            case 'launcher':
                pass

