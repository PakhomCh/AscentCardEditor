import xml.etree.cElementTree as xml
from constants import SETSIZE, COLORS, SHORTCOLORS
# Set Types:    Default     (50 cards + 5 tokens)
#               Core        (250 cards + 5 tokens)
#               Base        (36 cards)
#               Empty       (0 cards)
#               Custom      (Undetermined)

# Set Criteria  Name        Name of Set
#               Code        4-Symbol allcaps shortening of Name
#               Type        Set type from above
#               Release     Release period in "*-**" form

def NewSet(name='Unnamed', code='UNMD', settype='default', release='0-00'):

    # Create new set file and fill it with cards,
    # depending on set type

    # Adding copyright info


    # Setting up the kaset block
    setblock = xml.Element('kaset')
    setblock.set('name', name)
    setblock.set('code', code)
    setblock.set('type', settype)
    setblock.set('release', release)
    setblock.set('size', str(SETSIZE[settype][2]))
    setblock.insert(0, xml.Comment('CREATED AUTOMATICALLY WITH ASCENT SET EDITOR, COPYRIGHT KONTINUUM LLC'))
    

    # Setting up card block
    cardblock = xml.SubElement(setblock, 'cards')
    
    # Adding blank cards to set size
    cards = []
    cardcount = SETSIZE[settype][0]
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

        # Add color to array to keep it
        cards.append(card)
        
    # Setting up token block
    tokenblock = xml.SubElement(setblock, "tokens")

    # Adding blank tokens to set size
    tokencount = SETSIZE[settype][1]
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

        # Add color to array to keep it
        cards.append(card)
        
    # Saving set file
    tree = xml.ElementTree(setblock)
    filename = code + '.ace-set'
    tree.write(filename, encoding='utf-8')

NewSet()
