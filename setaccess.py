import sqlite3
from card import Card
from PIL import Image

class SetAccess:

    def __init__ (self, master):

        self.master = master
        self.load_db()
        # self.rerender()

    def rerender(self):

        for id in range(1, len(self.get_table())):

            values = self.get_card_values(id)
            print(self.get_card_values(id))

            with open('temp/temp.png', 'wb') as file:
                file.write(values[1])
            image = Image.open('temp/temp.png')

            card = Card(self.master, image, values[4], values[3], self.master.ingame['cardtypes'].index(values[5]), self.master.ingame['cardsubtypes'].index(values[6]), values[3], values[9], values[8], values[7])
            card.save_web()
            card.save_paper()

    def load_db(self, db_name = None):

        if db_name == None:

            
            self.DB = sqlite3.connect('sets/default_set.db')
            self.cursor = self.DB.cursor()

        else:

            self.DB = sqlite3.connect(db_name)
            self.cursor = self.DB.cursor()

    def close(self):

        self.DB.close()

    def add_card(self, card):

        cardnames = [x[2] for x in self.get_table()]
        name = card.tuple()[2]

        if name in cardnames:
            command = "UPDATE cards SET image = ?, cost = ?, color = ?, cardtype = ?, subtype = ?, textbox = ?, power = ?, artist = ? WHERE cardname = '" + name + "'"
            self.cursor.execute(command, card.shortuple())
        else:
            command = "INSERT INTO cards (id, image, cardname, cost, color, cardtype, subtype, textbox, power, artist) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            self.cursor.execute(command, card.tuple())

        self.DB.commit()
        print('EXECUTED')

    def delete_card(self, card_id):

        command = "DELETE FROM cards WHERE id = '" + str(card_id) + "'"
        self.cursor.execute(command)

        self.DB.commit()
        print("EXECUTED")

    def size(self):

        size = 0

        for i in self.cursor.execute('SELECT * FROM cards;'):
            size += 1

        return size

    def get_card_values(self, card_id):

        for i in self.cursor.execute('SELECT * FROM cards;'):
            if i[0] == card_id:
                return i

    def get_table(self):

        table = []

        for i in self.cursor.execute('SELECT * FROM cards;'):
            table.append(i)

        return table

    def get_data(self):

        table = []

        for i in self.cursor.execute('SELECT * FROM cards;'):
            table.append(i[2:9])

        return table
