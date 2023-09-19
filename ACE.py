from doctest import master
from window import Window
from setaccess import SetAccess
from dataccess import DatAccess

from launcher import Launcher
from designer import Designer

class AscentCardEditor():

    def __init__(self):
        
        # Legacy code
        # self.dat_access = DatAccess()
        # self.hotkeys = self.dat_access.hotkeys()
        # self.fonts = self.dat_access.fonts()
        # self.ingame = self.dat_access.ingame()
        # self.columns = self.dat_access.columns()
        # self.set_access = SetAccess(master = self)
        # self.color_themes = self.dat_access.color_themes()
        # self.window = Window(master = self)

        self.mode = 'launcher'

        # This status shows, if programm should start inner loop, held by another handler, 
        # like Launcher, Designer or Artist
        self.isrunning = True
        self.__setapp__()

    def __setapp__(self):
        match(self.mode):
            case 'designer':
                self.app = Designer(self)
            case 'artist':
                pass
            case 'launcher':
                self.app = Launcher(self)
        
    def SwapMode(self, mode):
        self.mode = mode
        self.__setapp__()
        self.isrunning = True

    def Run(self):
        while self.isrunning:
            # Set status variable to show that no other handler is gonna be open after this one
            self.isrunning = False
            self.app.Run()

    def Exit(self):

        pass