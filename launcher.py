from uifactory import CoreWindow

# Launcher GUI that lets user to choose operating mode and set to work on
class Launcher():
    def __init__(self):
        self.window = CoreWindow(self, 'launcher')
    
    def Run(self):        
        self.window.mainloop()    
    
    def UpdateSetFiles(self):        
        pass    
    
    def Retrieve(self, data):        
        pass