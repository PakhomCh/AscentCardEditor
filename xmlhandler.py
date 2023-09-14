import xml.etree.cElementTree as xml

# Class to handle xml tree objects for app to edit, view and save/load
class SetHandler():

    def __init__(self, set=None):

        self.tree = set

    # Prints current tree into console, if tree exists
    # Function created for debugging purpose
    def Log(self):
        if self.tree is not None:
            xmlstring = xml.tostring(self.tree.getroot())
            print(xmlstring)
        else:
            print('SetHandler is unconnected to a set.')

    # Loads set from set folder, by set code
    def Load(self, code='UNMD'):
        self.tree = xml.parse('sets/' + code + '.ace-set')
