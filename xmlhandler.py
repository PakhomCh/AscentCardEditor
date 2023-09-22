import xml.etree.cElementTree as xml
from constants import SETSIZE, COLORS, SHORTCOLORS

# Class to handle xml tree objects for app to edit, view and save/load
class SetHandler():

    def __init__(self, set=None):

        self.tree = set

    # Checks if Handler is connected to a database
    def IsConnected(self):
        return False if self.tree == None else True

    # Prints current tree into console, if tree exists
    # Function created for debugging purpose
    def Log(self):
        if self.IsConnected():
            xmlstring = xml.tostring(self.tree.getroot())
            print(xmlstring)
        else:
            print('SetHandler is unconnected to a set.')

    # Loads set from set folder, by set code
    def Load(self, code='UNMD'):
        self.tree = xml.parse('sets/' + code + '.ace-set')

    # Saves .ace-set file to sets folder, using set code
    def Save(self):
        if self.IsConnected():
            root = self.tree.getroot()
            code = root.attrib['code']
            filename = 'sets/' + code + '.ace-set'
            self.tree.write(filename, encoding='utf-8')
    
    # Clears database from handler
    def Drop(self):
        self.tree = None

    # Set Types:    Default     (50 cards + 5 tokens)
    #               Core        (250 cards + 10 tokens)
    #               Base        (36 cards)
    #               Empty       (0 cards)
    #               Custom      (Undetermined)

    # Set Criteria  Name        Name of Set
    #               Code        4-Symbol allcaps shortening of Name
    #               Type        Set type from above
    #               Release     Release period in "*-**" form

    def New(self, name='Unnamed', code='UNMD', settype='default', release='0-00'):
        
        # Create new set file and fill it with cards,
        # depending on set type

        # Setting up the kaset block
        setblock = xml.Element('kaset')
        setblock.set('name', name)
        setblock.set('code', code.upper())
        setblock.set('type', settype.lower())
        setblock.set('release', release)
        setblock.set('size', str(SETSIZE[settype.lower()][2]))
        
        # Adding copyright info
        setblock.insert(0, xml.Comment('CREATED AUTOMATICALLY WITH ASCENT SET EDITOR, COPYRIGHT KONTINUUM LLC'))
    
        # Setting up card block
        cardblock = xml.SubElement(setblock, 'cards')
    
        # Adding blank cards to set size
        cards = []
        cardcount = SETSIZE[settype.lower()][0]
        for itera in range(cardcount):
        
            cardcolor = COLORS[itera // (cardcount // 5)]
            letter = SHORTCOLORS[itera // (cardcount // 5)]
        
            # Create and set blank card, filling each ingame color equally
            card = xml.SubElement(cardblock, 'card')
            card.set('id', str(itera))
            card.set('name', letter + str(itera % (cardcount // 5)))
            card.set('color', cardcolor)
            card.set('power', 'X')
            card.set('text', '')
            card.set('cost', '')
            card.set('type', '')
            card.set('subtype', '')
            card.set('art', '')
            card.set('istoken', '0')

            # Add card to array to keep it
            cards.append(card)
        
        # Setting up token block
        tokenblock = xml.SubElement(setblock, "tokens")

        # Adding blank tokens to set size
        tokencount = SETSIZE[settype.lower()][1]
        for itera in range(tokencount):
        
            cardcolor = COLORS[itera // (tokencount // 5)]
            letter = SHORTCOLORS[itera // (tokencount // 5)]
        
            # Create and set blank token, filling each ingame color equally
            token = xml.SubElement(tokenblock, 'card')
            token.set('id', str(itera + cardcount))
            token.set('name', 'T' + letter + str(itera % (cardcount // 5)))
            token.set('color', cardcolor)
            token.set('power', 'X')
            token.set('text', '')
            token.set('cost', '')
            token.set('type', '')
            token.set('subtype', '')
            token.set('art', '')
            token.set('istoken', '1')

            # Add card to array to keep it
            cards.append(card)
        
        # Saving set tree
        self.tree = xml.ElementTree(setblock)

    def CardTable(self):
        root = self.tree.getroot()
        cards = root.find('cards')
        table = []
        for itera in cards:
            card = [x[1] for x in itera.items()[0 : -2]]
            table.append([card[0], card[1], card[5], card[2], card[6], card[7], card[4], card[3]])
        return table

    # FINISH THIS ONE
    def Fetch(self, something):
        pass
    
