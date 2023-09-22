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