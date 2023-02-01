import sqlite3

class DatAccess:

    def __init__ (self):

        self.__load_db()

    def hotkeys(self):

        table = []

        for i in self.cursor.execute('SELECT * FROM hotkeys;'):
            table.append(i)

        results = {}
            
        for i in table:
            results[i[0]] = {'b': 'ctrl+' + i[1].upper(), 'c': '<Control-' + i[1].lower() + '>'}

        return results

    def fonts(self):

        table = []

        for i in self.cursor.execute('SELECT * FROM fonts;'):
            table.append(i)

        results = {}
            
        for i in table:
            results[i[0]] = (i[1], i[2])

        return results

    def ingame(self):

        results = {}

        results['cardtypes'] = self.__card_types()
        results['cardsubtypes'] = self.__card_subtypes()
        results['colors'] = self.__card_colors()
        results['keywords'] = self.__keywords()

        return results

    def columns(self):

        table = []

        for i in self.cursor.execute('SELECT * FROM tablecolumns;'):
            table.append(i)

        results = {'names': [], 'width': {}}
            
        for i in table:
            results['names'].append(i[0])
            results['width'][i[0]] = i[1]

        return results

    def color_themes(self):

        table = []

        for i in self.cursor.execute('SELECT * FROM colorthemes;'):
            table.append(i)

        results = {'themes': [], 'colors': {}}
            
        for i in table:
            results['themes'].append(i[0])
            results['colors'][i[0]] = [i[1], i[2], i[3], i[4]]

        return results

    def close(self):

        self.DB.close()

    def __load_db(self):

        self.DB = sqlite3.connect('data/appdata.db')
        self.cursor = self.DB.cursor()

    def __get_table(self, requested):

        table = []

        for i in self.cursor.execute('SELECT * FROM ' + requested + ';'):
            table.append(i[0])

        return table

    def __card_types(self):

        return self.__get_table('cardtypes')

    def __card_subtypes(self):

        fractions = sorted(self.__get_table('fractions'))
        creaturetypes = sorted(self.__get_table('unittypes'))
        ordertypes = sorted(self.__get_table('ordertypes'))
        relictypes = sorted(self.__get_table('relictypes'))

        results = [' ————— '] + ordertypes + [' ————— '] + relictypes + [' ————— '] + creaturetypes + [' ————— '] + fractions

        return results
    
    def __card_colors(self):

        return self.__get_table('colors')

    def __keywords(self):
        
        table = []

        for i in self.cursor.execute('SELECT * FROM keywords;'):
            table.append(i)

        results = {'words': [], 'rules': {}}
            
        for i in table:
            results['words'].append(i[0])
            results['rules'][i[0]] = i[1]

        results['words'] = sorted(results['words'])

        return results