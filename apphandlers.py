from uifactory import CoreWindow

class AppHandler():
    def __init__(self, master, windowtype):
        self.master = master
        self.window = CoreWindow(self, windowtype)
    
    def Run(self):        
        self.window.mainloop()
    
    def SwapMode(self, mode):        
        if mode != None:
            self.master.SwapMode(mode)