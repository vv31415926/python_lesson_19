from flask import Flask
from flask import render_template, url_for, request
import datetime
from person import Person
from my_lib import get_week
from parser_price import Parser_price
from head_hunter_vacancies import HeadHunter_vacancies
from bd_apartment import Appartment_BD

from sqlalchemy import  create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, View_apartment, Country, Region, City, Address, Characteristic


pers = Person()

app = Flask( __name__ )


engine = create_engine('sqlite:///apartment.db?check_same_thread=False')
Base.metadata.bind = engine
DBSession = sessionmaker( bind=engine )
session = DBSession()

@app.route("/")
@app.route("/index/")
def main_win():   # Главная страница
    today = datetime.datetime.today()
    scw = get_week( int( today.strftime('%w') ) )
    return render_template( 'index.html',  curdate = today.strftime('%d-%m-%Y'), curweek = scw )

@app.route("/personal/")
def pers_win():  # Персональные данные -------------------------------------------------------
    dic={
    'photo' : pers.get_photo(),
    'fio' : pers.get_name() + ' ' + pers.get_otch() + ' ' + pers.get_fam(),
    'birthday' : pers.get_birthday(),
    'attach': pers.get_attach()
    }
    return render_template( 'personal.html', **dic )

@app.route("/parser/" )
def parser():   # начальная страница парсера квартир - выбор района ---------------------------
    return render_template( 'parser_form.html' )

@app.route("/price_apartments/", methods=['POST'] )
def price():  # результат работы парсера - цены
    region = request.form['region']   # получение параметра

    parser = Parser_price( region )   # создать объект парсинга
    dicMin = parser.cost_min(rej='dic')
    dicMax = parser.cost_max(rej='dic')

    # параметры для страницы
    dic={}
    dic['region'] = region
    dic['minprice'] = dicMin['price']
    dic['mincity'] = dicMin['city']
    dic['mincharact'] = dicMin['address']+'; '+dicMin['region']+'; '+dicMin['characteristic']
    dic['maxprice'] = dicMax['price']
    dic['maxcity'] = dicMax['city']
    dic['maxcharact'] = dicMax['address'] + '; ' + dicMax['region'] + '; ' + dicMax['characteristic']

    return render_template( 'price_apartments.html', **dic )

@app.route("/hh_main/" )
def hh_main():   # начальная страница выкансий  API  ---------------------------------------------
    return render_template('hh_city.html')


@app.route("/hh_vacancy/", methods=['POST'] )
def hh_vacancy():
    city = request.form['city']   # какой город был выбран
    vac = request.form['vac']

    hh = HeadHunter_vacancies()

    lst, num, sum = hh.view_vacancies( city, vac )
    dic={}
    s = ''
    for v in lst:
        if v:
            s += '* '+v+'\n'
    dic['skills'] = s
    dic['city'] = city
    dic['vac'] = vac
    if num == 0:
        dic['salary'] = 0.0
    else:
        dic['salary'] = round( sum/num, 2 )

    return render_template('hh_vacancy.html', **dic)


@app.route("/bd_apartment/" )
def bd_apartment():
    return render_template('bd_apartment.html')

@app.route("/bd_apartment_view/", methods=['POST'] )
def bd_apartment_view():
    region = request.form['region']  # получение параметра
    load  = request.form.get('load')  # получение параметра

    dic = {}
    bd = Appartment_BD( )

    dic['field'] = []
    if bd.is_connect == 'OK':
        lstField = bd.get_title_table()  # список кортежей(записей) с полями внутри
        dic['field']=lstField

    # данные БД
    # перезаписать
    if load:
        parser = Parser_price( )  # создать объект парсинга по району
        lst_data = parser.data_search( region )
        bd.save_data(  lst_data )

    lst_view_data, update = bd.get_data( region )
    dic['data'] = lst_view_data
    dic['region'] = region
    dic['update'] = update

    return render_template('bd_apartment_view.html', **dic)


#----------------------------------------------------------------------------------------- SALAlchemy
def get_field():
    #print('============ Поля просмотра =======================')
    lst_field = session.query(View_apartment).all()
    lst=[]
    for field in lst_field:
        #print(field.colname, field.coltitle, sep=', ')
        lst.append( {'npp':field.npp, 'name':field.colname, 'title':field.coltitle} )
    lst = sorted(  lst, key=lambda x: x['npp']  )  # сортировка по порядку
    return lst

def get_country():
    query = session.query(City, Country)
    query = query.join(City, City.id_country == Country.id)
    records = query.all()
    lst=[]
    for city, country in records:
        #print(city, country, sep=', ')
        lst.append( {'city':city, 'country':country} )
    return lst

def get_region( name, session ):
    reg = session.query(Region).filter( Region.name == name).first()
    lst=[]
    if reg:
        lst = [reg.id, reg.name, reg.id_city, reg.date]

    return lst

def get_data( region, session ):
    reg = get_region( region, session )
    records = []
    upd=''
    if reg:
        id_reg = reg[0]
        upd = reg[3]

        query = session.query( Characteristic, Address ).filter( Address.id_region == id_reg )
        query = query.join( Address, Address.id == Characteristic.id_address )
        records = query.all()
        # for char, address in records:
        #     print( address, char,  sep='; ')
    return (records, upd)

def save_data( lst:list, session): #
    s1 = lst[0]['region'].replace( ',',' ' )
    reg = ' '.join(  s1.split(' ')[0:2]  )
    id_reg = set_region( reg, session )

    for v in lst:
        id_addr = set_address( id_reg, v['address'], session )
        id_charact = set_characteristic( id_addr, v['characteristic'], session)

def set_region( name:str, session:DBSession ):
    reg = get_region( name, session )
    id_reg = None
    if reg:
        id_reg = reg[0]
    else:  # нет такого района
        today = datetime.datetime.today().strftime('%d-%m-%Y')
        reg = Region( name=name, id_city=1, date=today)
        session.add( reg )
        session.commit()
        reg = get_region( name, session )
        if reg:
            id_reg = reg[0]
    return id_reg

def get_address( name, id_city, session ):
    adr = session.query(Address).filter( Address.name == name).first()
    lst=[]
    if adr:
        lst = [adr.id, adr.name, adr.id_city, adr.id_region]

    return lst

def set_address( id_reg, name, session:DBSession ):
    adr = get_address( name, 1, session )
    id_adr = None
    if adr:
        id_adr = adr[0]
    else:  # нет такого
        adr = Address( name=name, id_city=1, id_region=id_reg )
        session.add(adr)
        session.commit()
        adr = get_address(name, 1,  session )
        if adr:
            id_adr = adr[0]

    return id_adr

def get_characteristic( id_addr,  session ):
    ch = session.query(Characteristic).filter( Characteristic.id_address == id_addr).first()
    lst=[]
    if ch:
        lst = [ch.id, ch.data]

    return lst

def set_characteristic( id_addr, data, session ):
    ch = get_characteristic( id_addr, session)
    id_ch = None
    if ch:
        id_adr = ch[0]
    else:  # нет такого
        ch = Characteristic( data=data, id_address=id_addr )
        session.add( ch )
        session.commit()
        ch = get_characteristic( id_addr, session )
        if ch:
            id_ch = ch[0]

    return id_ch

@app.route("/sqlalchemy_apartment/")
def sqlalchemy_apartment():
    return render_template('sqlalchemy_apartment.html')



@app.route("/sqlalchemy_apartment_view/", methods=['POST'])
def sqlalchemy_apartment_view():
    region = request.form['region']  # получение параметра
    load = request.form.get('load')  # получение параметра

    dic = {}

    dic['region'] = region

    dic['field'] = []
    lstField = get_field()
    lst = []
    for v in lstField:
        lst.append(v['title'])
    dic['field'] = lst



    # данные БД
    # перезаписать
    if load:
        parser = Parser_price()  # создать объект парсинга по району
        lst_data = parser.data_search(region)
        save_data( lst_data, session )

    #print(  bd.get_id_region( region ) )
    lst_view_data, update = get_data( region, session )
    dic['data'] = lst_view_data
    dic['region'] = region
    dic['update'] = update

    return render_template('sqlalchemy_apartment_view.html', **dic)




# ********************************************************************
if __name__ == "__main__":
    #print( 'версия:', flask.__version__ )
    app.run( debug=True )
    #Thread(target=app.polling, args=()).start()