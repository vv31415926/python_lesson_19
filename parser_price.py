import requests
import pprint
from bs4 import BeautifulSoup
from bd_apartment import Appartment_BD

class Parser_price:
    def __init__(self, region=None ):
        self._domain = 'https://chelyabinsk.n1.ru'
        self._region = region
        self._lst_result = []
        self._ini_dic()


    def _ini_dic(self):
        dic = {}
        dic['region'] = ''
        dic['city'] = ''
        dic['address'] = ''
        dic['characteristic'] = ''
        dic['price'] = ''
        return dic

    def _url_region(self, reg ):
        r_url='-'
        if reg == 'Калининский район':
            r_url = 'Kalininskiy'
        if reg == 'Курчатовский район':
            r_url = 'Kurchatovskiy'
        if reg == 'Ленинский район':
            r_url = 'Leninskiy'
        if reg == 'Металлургический район':
            r_url = 'Metallurgicheskiy'
        if reg == 'Советский район':
            r_url = 'Sovetskiy'
        if reg == 'Тракторозаводский район':
            r_url = 'Traktorozavodskiy'
        if reg == 'Центральный район':
            r_url = 'Centralnyi'

        return r_url

    def data_search(self, region:str=None):
        if region:
            self._region = region
        region_url = self._url_region( self._region )

        URL = f'{self._domain}/kupit/kvartiry/vtorichka/district-{region_url}-rayon/'
        response = requests.get(URL)
        ttt = response.text
        soup = BeautifulSoup(response.text, 'html.parser')


        div_tags = soup.find_all('div', class_='living-list-card__main-container')

        self._lst_result = []
        for v1 in div_tags:
            dic = self._ini_dic()

            tags = v1.find('a', class_='link')
            #print(tags.text)
            if tags:
                dic['address'] = tags.text

            tags = v1.find('div', class_='search-item-district')
            #print(  tags.text )
            if tags:
                dic['region'] = tags.text

            tags = v1.find('div', class_='living-list-card__city-with-estate')
            #print(tags.text)
            if tags:
                dic['city'] = tags.text

            tags = v1.find('div', class_='living-list-card__area')
            if tags:
                #print(tags.text)
                dic['characteristic'] += tags.text

            tags = v1.find('div', class_='living-list-card__floor')
            if tags:
                #print(tags.text)
                dic['characteristic'] += " " + tags.text

            tags = v1.find('div', class_='living-list-card__material')
            if tags:
                #print(tags.text)
                dic['characteristic'] += " " + tags.text

            tags = v1.find('div', class_='living-list-card-price__item _object')
            #print(tags.text)
            if tags:
                dic['price'] = (tags.text).replace(chr(160), ' ') + 'руб'
            else:
                dic['price'] = ('0 ') + 'руб'

            self._lst_result.append(dic)

        #print('-------------------------------------------------------------------------------')
        #pprint.pprint( self._lst_result )
        return self._lst_result

    def cost_min(self, rej = 'str' ):
        s=''
        sn=''
        lst=[]
        t = 0

        r = []
        lst = self.data_search()

        vMin = [999999999999.0,-1]

        for i,v in enumerate(lst):
            s = v['price'].replace(' ','')
            sn = s[:-3]
            t = float( sn )
            if t < vMin[0]:
                vMin[0] = t
                vMin[1] = i

        if vMin[1] == -1:
            return r
        else:
            if rej == 'str':   #  вывод в режиме строки
                d = lst[vMin[1]]
                s = 'минимальная цена: ' + d['price'] + '\n'
                s += 'город: ' + d['city'] + '\n'
                s += d['address'] + '\n'
                s += d['region'] + '\n'
                s += 'характеристика: ' + d['characteristic']
                r = s
            else:   #  вывод в режиме словаря
                d = lst[vMin[1]]
                r = d
        return r

    def cost_max( self, rej = 'str' ):
        r = []
        lst = self.data_search()
        vMax = [0.0,-1]

        for i,v in enumerate(lst):
            s = v['price'].replace(' ','')
            sn = s[:-3]
            t = float( sn )
            if t > vMax[0]:
                vMax[0] = t
                vMax[1] = i

        if vMax[1] == -1:
            return []
        else:
            if rej == 'str':  # вывод в режиме строки
                d = lst[ vMax[1] ]
                s = 'максимальная цена: '+ d['price']+'\n'
                s += 'город: ' + d['city']+ '\n'
                s += d['address']+'\n'
                s += d['region'] + '\n'
                s += 'характеристика: '+d['characteristic']
                r = s
            else:    #  вывод в режиме словаря
                d = lst[vMax[1]]
                r = d

            return r

    def save_bd(self):
        bd  = Appartment_BD()
        bd.ini_connect()
        lst = self.data_search()   # список словарей. элемент списка - запись, словарь - поля записи

        bd.save_record( lst )






if __name__ == '__main__':
    p = Parser_price('Калининский')
    sMin = p.cost_min()
    sMax = p.cost_max()
    print('\n*********************************************************************')
    print(  sMin  )
    print(sMax)






