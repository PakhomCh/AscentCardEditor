from uifactory import CoreWindow
from apphandlers import AppHandler

class Designer(AppHandler):
    def __init__(self, master):
        super().__init__(master, 'designer')
        
# I do not know, why this file exists
# It is nit implemented anywhere