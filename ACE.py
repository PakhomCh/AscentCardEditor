from doctest import master
from window import Window
from setaccess import SetAccess
from dataccess import DatAccess

class AscentCardEditor():

    def __init__(self):
        
        self.dat_access = DatAccess()
        self.hotkeys = self.dat_access.hotkeys()
        self.fonts = self.dat_access.fonts()
        self.ingame = self.dat_access.ingame()
        self.columns = self.dat_access.columns()
        self.set_access = SetAccess(master = self)
        self.color_themes = self.dat_access.color_themes()
        self.window = Window(master = self)
        
    def run(self):

        self.window.run()

    def exit(self):

        self.set_access.close()
        self.dat_access.close()
        self.window.close()