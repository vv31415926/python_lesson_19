import requests
import pprint

class HeadHunter_vacancies:
    def __init__(self):
        self.baseURL = 'https://api.hh.ru'
        self.vacancyURL = f'{self.baseURL}/vacancies'
        self.country = 'Россия'

        self.cur_city=['','']
        self.cur_vacancy = ['','']

    def view_vacancies( self, city:str, vac:str ):
        idCountry, idRegion, idCity = self.get_id( city ) # ID заданного города
        num = 0
        #set_vac = set([])
        sum = 0.0
        skills = set([])
        for ind_page in range(100):
            params = {
                #'text': 'NAME:'+vac,
                'per_page': 50,
                'page': ind_page,
                'area': idCity
            }
            response = requests.get( self.vacancyURL, params=params).json()
            if 'items' in response:
                items = response['items']   # список словарей вакансий
                #print(  len(items), len(set_vac) )

                for v in items:     # по элементам словаря
                    name = v['name']
                    if 'salary' in v:

                        y = False
                        if v['salary']:
                            if 'from' in v['salary']:
                                if v['salary']['from']:
                                    y = True
                                    sum += v['salary']['from']
                                    num += 1
                            if not y:
                                if 'to' in v['salary']:
                                    if v['salary']['to']:
                                        y = True
                                        sum += v['salary']['to']
                                        num += 1

                    if 'snippet' in v:
                        #print( '----',num, sum, 'snippet' in v )
                        if 'requirement' in v['snippet']:
                            z = v['snippet']['requirement']
                            if z:
                                lst = z.split( '.' )
                                for s in lst:
                                    skills.add( s )
            else:
                break

        #print( len(skills), num, sum )
        return (list( skills ), num, sum)


    def get_id( self, nameCity:str ):
        # [{'areas'Страна: [{'areas'j,область/край/республика : [{'areas'Город: [],
        url_area = f'{self.baseURL}/areas'
        response = requests.get(url_area).json()   # список [0] из словарей стран

        res = ''
        for dicCountrys in response: # по словарям стран
            if dicCountrys['name'] == self.country:
                # словарь областей нужной страны
                idCountry = dicCountrys['id']  # ID нужной страны
                lstRegions = dicCountrys['areas'] # список словарей областей

                for dicRegion in lstRegions:
                    # словарь области с городами

                    #print( dicRegion['name'], nameCity )
                    if dicRegion['name'] == nameCity:
                        # Нужный город  - областной
                        idRegion = dicRegion['parent_id']
                        idCity = dicRegion['id']
                        res = (idCountry, idRegion, idCity)
                        break

                    lstCitys = dicRegion['areas']   # список словарей городов
                    for dicCity in lstCitys:
                        # словарь города
                        if dicCity['name'] == nameCity:
                            # нужный город
                            idRegion = dicCity['parent_id']
                            idCity = dicCity['id']
                            res = (idCountry, idRegion, idCity )
                            break
                    if res:
                        break
                if res:
                    break
            if res:
                break

        if res:
            self.cur_city = [res[2], nameCity]  # Запомнить выбор города

        return res


    def get_cur_city(self):
        return self.cur_city
    def set_cur_city(self, id, name ):
        self.cur_city = [id, name]

    def get_cur_vacancy(self):
        return self.cur_vacancy
    def set_cur_vacancy(self, id, name ):
        self.cur_vacancy = [id, name]

if __name__ == '__main__':
    hh = HeadHunter_vacancies()

    r = hh.get_id_Region( 'Москва' )
    print( r )

    #r = hh.view_vacancies('Челябинск')
    #print( len(r) )
    #pprint.pprint( r )