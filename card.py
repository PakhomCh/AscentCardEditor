from PIL import Image, ImageFont
from PIL.ImageDraw import Draw
from os import remove



class Card():

    def __init__ (self, master, artwork, color = 0, cost = '', cardtype = 0, subtype = 0, name = '', artist = '', power = '', ruletext = ''):

        self.master = master
        self.image = artwork.copy()
        self.name = name
        self.color = color
        self.cost = cost
        self.cardtype = cardtype
        self.subtype = subtype
        self.artist = artist
        self.power = power
        self.ruletext = ruletext

    def build(self):

        art = self.image.copy()

        self.__add_color()      # Флажок
        self.__add_cost()       # Стоимость карты
        self.__add_type()       # Тип карты
        self.__add_title()      # Название карты
        self.__add_subtype()    # Подтип карты
        self.__add_ruletext()   # Текст карты
        self.__add_power()      # Сила карты
        self.__add_credits()    # Автор арта
        self.__add_copyright()  # Копирайт

        result = self.image
        self.image = art

        return result

    def save_web(self):

        if self.name == '':
            cardname = 'results/web/untitled.png'
        else:
            cardname = 'results/web/' + self.name.replace(':', '') + '.png'
        x_shift = 15
        y_shift = 15
        self.build().crop((x_shift, y_shift, x_shift + 744, y_shift + 1039)).save(cardname)

    def save_paper(self):

        if self.name == '':
            cardname = 'results/paper/untitled.png'
        else:
            cardname = 'results/paper/' + self.name.replace(':', '') + '.png'
        self.build().save(cardname)

    def tuple(self):

        self.image.save('temp/temp.png')
        with open('temp/temp.png', 'rb') as file:
            image_data = file.read()
        remove('temp/temp.png')

        id_data = self.master.set_access.size() + 1
        color_data = self.master.ingame['colors'][self.color]
        cardtype_data = self.master.ingame['cardtypes'][self.cardtype]
        subtype_data = self.master.ingame['cardsubtypes'][self.subtype]

        return (id_data, image_data, self.name, self.cost, color_data, cardtype_data, subtype_data, self.ruletext, self.power, self.artist)

    def shortuple(self):

        longtuple = [*self.tuple()]

        return [longtuple[1]] + longtuple[3:]

    def __add_title(self):

        x_limit = 445
        y_limit = 45
        fontsize = 100

        draw = Draw(self.image)

        font = ImageFont.truetype('fonts/Colus.ttf', fontsize)

        x, y = draw.textsize(self.name, font = font)
        while x > x_limit or y > y_limit:
            fontsize -= 1
            font = ImageFont.truetype('fonts/Colus.ttf', fontsize)
            x, y = draw.textsize(self.name, font = font)

        draw.text((175 + (x_limit - x) // 2, 67 + (y_limit - y) // 2), self.name, font = font)
        
    def __add_subtype(self):

        x_limit = 670
        y_limit = 40
        fontsize = 100
        subtype = self.master.ingame['cardsubtypes'][self.subtype]

        draw = Draw(self.image)

        font = ImageFont.truetype('fonts/Colus.ttf', fontsize)
        x, y = draw.textsize(subtype, font = font)
        while x > x_limit or y > y_limit:
            fontsize -= 1
            font = ImageFont.truetype('fonts/Colus.ttf', fontsize)
            x, y = draw.textsize(subtype, font = font)

        draw.text((55 + (x_limit - x) // 2, 644 + (y_limit - y) // 2), subtype, font = font)

    def __add_credits(self):

        x_limit = 300
        y_limit = 30
        fontsize = 100
        if self.artist == '':
            self.artist = 'unknown'
        artline = 'Арт: ' + self.artist + ', ТЕСТ'

        draw = Draw(self.image)

        font = ImageFont.truetype('fonts/Spectral-Regular.ttf', fontsize)
        x, y = draw.textsize(artline, font = font)
        while x > x_limit or y > y_limit:
            fontsize -= 1
            font = ImageFont.truetype('fonts/Spectral-Regular.ttf', fontsize)
            x, y = draw.textsize(artline, font = font)
        draw.text((232 + (x_limit - x) // 2, 950 + (y_limit - y) // 2), artline, font = font, fill = 'black')

    def __add_copyright(self):

        x_limit = 300
        y_limit = 30
        line = 'Восхождение™'

        draw = Draw(self.image)

        font = ImageFont.truetype('fonts/Spectral-Regular.ttf', 22)
        x, y = draw.textsize(line, font = font)
        draw.text((232 + (x_limit - x) // 2, 972 + (y_limit - y) // 2), line, font = font, fill = 'black')

    def __add_power(self):

        x_limit = 71
        y_limit = 103
        fontsize = 40

        draw = Draw(self.image)

        font = ImageFont.truetype('fonts/Spectral-Regular.ttf', fontsize)
        x, y = draw.textsize(str(self.power), font = font)

        draw.text((617 + (x_limit - x) // 2, 828 + (y_limit - y) // 2), str(self.power), font = font, fill = (58, 57, 57))

    def __BuildRuletext(self, image, words, x_limit, y_limit, fontsize):

        result = ''

        draw = Draw(image)

        for i in words:

            temp = result + i + ' '

            font = ImageFont.truetype('fonts/Spectral-Regular.ttf', fontsize)
            x, y = draw.textsize(temp, font = font)
        

            if y > y_limit:
                return self.__BuildRuletext(image, words, x_limit, y_limit, fontsize - 2)

            if x > x_limit:
                temp = result + '\n' + i + ' '

                font = ImageFont.truetype('fonts/Spectral-Regular.ttf', fontsize)
                x, y = draw.textsize(temp, font = font)

                if x > x_limit or y > y_limit:
                    return self.__BuildRuletext(image, words, x_limit, y_limit, fontsize - 2)

            result = temp

        return result, fontsize

    def __add_ruletext(self):
    
        text = self.ruletext

        x_limit = 495
        y_limit = 235
        fontsize = 40
        words = text.replace('\n', ' \n').split(' ')
        result = ''

        draw = Draw(self.image)

        font = ImageFont.truetype('fonts/Spectral-Regular.ttf', fontsize)

        result, fontsize = self.__BuildRuletext(self.image, words, x_limit, y_limit, fontsize)

        font = ImageFont.truetype('fonts/Spectral-Regular.ttf', fontsize)

        temp = ''
        result = result.split(' ')
        result.append('')
    
        
        for i in range(len(result) - 1):
            flag = 0
            for kw in self.master.ingame['keywords']['words']:
                if kw in result[i]:
                    flag = 1
            if flag == 1:
                temp += '*' + result[i] + ' '
                result[i + 1] = '!' + result[i + 1]
            else:
                temp += result[i] + ' '
        result = temp
        
        lines = result.split('\n')
        line_height = 0

        for i in range(len(lines)):
            line = lines[i]

            words = line.split(' ')
            line_weight = 0

            for j in words:
                word = j + ' '

                while '*' in word or '_' in word or '!' in word:
                    flag = 0
                    if word[0] == '*':
                        word = word[1:]
                        font = ImageFont.truetype('fonts/spectral/Spectral-Bold.ttf', fontsize)
                        flag = 1
                    elif word[0] == '_':
                        word = word[1:]
                        font = ImageFont.truetype('fonts/spectral/Spectral-LightItalic.ttf', fontsize)
                        flag = 1
                    elif word[0] == '!':
                        word = word[1:]
                        font = ImageFont.truetype('fonts/Spectral-Regular.ttf', fontsize)
                        flag = 1
                    if flag == 0:
                        break
            
                match word:
                    case '-- ':
                        word = '— '


                draw.text((109 + line_weight, 705 + line_height), word, font = font, fill = 'black')
                line_weight += draw.textsize(word, font)[0]
            
            line_height += y_limit // len(lines) 

    def __add_color(self):

        match self.color:
            case 4:
                frame = Image.open('data/FrameW.png')
            case 3:
                frame = Image.open('data/FrameB.png')
            case 2:
                frame = Image.open('data/FrameU.png')
            case 1:
                frame = Image.open('data/FrameR.png')
            case 0:
                frame = Image.open('data/FrameN.png')

        mask = Image.open('data/FrameMask.png').convert('L')
        self.image.paste(frame, (15, 15), mask)

    def __add_cost(self):

        if self.cost == '':
            frame = Image.open('data/Coin.png')
        else:
            frame = Image.open('data/' + str(self.cost) + '.png')
        mask = Image.open('data/CoinMask.png').convert('L')
        self.image.paste(frame, (15, 15), mask)

    def __add_type(self):
        match self.cardtype:
            case 0:
                cardtype = 'Unit'
            case 1:
                cardtype = 'City'
            case 2:
                cardtype = 'Order'
            case 3:
                cardtype = 'Rite'
            case 4:
                cardtype = 'Relic'

        frame = Image.open('data/' + cardtype + '.png')
        mask = Image.open('data/' + cardtype + 'Mask.png').convert('L')
        self.image.paste(frame, (15, 15), mask)

        