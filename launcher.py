import os
from uifactory import CoreWindow
from xmlhandler import SetHandler
from apphandlers import AppHandler

# Launcher GUI that lets user to choose operating mode and set to work on
class Launcher(AppHandler):
    def __init__(self, master):
        super().__init__(master, 'launcher')
    
    def UpdateSetFiles(self):        
        pass    

    def NewSet(self):
        handler = SetHandler()
        handler.New()
        handler.Save()

    def GetSetFileNames(self):
        filenames = [x.split('.ace-set')[0] for x in os.listdir('.\sets') if '.ace-set' in x]
        return filenames