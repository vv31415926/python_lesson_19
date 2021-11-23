import datetime

#from sqlalchemy.schema import  MetaData
from sqlalchemy import Column, Integer, String, Float, create_engine,Table, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapper, sessionmaker, create_session



engine = create_engine( 'sqlite:///apartment.db', echo=False )
Base = declarative_base()

metadata = MetaData( bind=engine )

class View_apartment( Base ):
    __table__ = Table( 'View_apartment', metadata, autoload=True )

    def __init__( self, npp, colname, coltitle ):
        self.npp = npp
        self.colname = colname
        self.coltitle = coltitle

    def __str__(self):
        return f'{self.coltitle}'

class Region( Base ):
    __table__ = Table('Region', metadata, autoload=True )

    def __init__( self, name, id_city ):
        self.name = name
        self.id_country = id_city

    def __str__(self):
        return f'{self.name}'

class City( Base ):
    __table__ = Table('City', metadata, autoload=True )

    def __init__( self, name, id_country ):
        self.name = name
        self.id_country = id_country

    def __str__(self):
        return f'{self.name}'

class Country( Base ):
    __table__ = Table( 'Country', metadata, autoload=True )
    def __init__(self, name  ):
        self.name = name

    def __str__(self):
        return f'{self.name}'

class Address( Base ):
    __table__ = Table( 'Address', metadata, autoload=True )
    def __init__(self, id_region, id_city, name  ):
        self.id_region = id_region
        self.id_city = id_city
        self.name = name

    def __str__(self):
        return f'{self.name}'

class Characteristic( Base ):
    __table__ = Table( 'Characteristic', metadata, autoload=True )
    def __init__(self, id_address, data  ):
        self.id_address = id_address
        self.data = data

    def __str__(self):
        return f'{self.data}'

#session = create_session( bind=engine )
Session = sessionmaker( bind=engine )
session = Session()

print( '============ Поля просмотра =======================' )
lst_field = session.query( View_apartment ).all()
for field in lst_field:
   print( field.colname, field.coltitle, sep=', ' )

print( '============  Страна =======================' )
lst_country = session.query( Country ).all()
for country in lst_country:
    print(country)

print( '============  Город =======================' )
# Вариант 1:
# lst_city = session.query( City ).all()
# for city in lst_city:
#     country = session.query(Country).filter_by( id = city.id_country ).first()
#     print( country.name, city.name, sep=', ' )
# Вариант 2:
query = session.query(  City, Country )
query = query.join( City,  City.id_country == Country.id )
records = query.all()
for city, country in records:
    print( city, country, sep=', ' )


print( '============  Регион =======================' )
# Вариант 1:
# lst_region = session.query( Region ).all()
# for region in lst_region:
#     city = session.query(City).filter_by( id = region.id_city ).first()
#     country = session.query(Country).filter_by(id=city.id_country).first()
#     print(city.name, region.name, country.name, sep=', ' )
# Вариант 2:
query = session.query(  Region,City  )
query = query.join( City, Region.id_city == City.id  )
records = query.all()
for reg, city in records:
    print( city, reg, sep=', ' )

print( '============  Адрес =======================' )
# Вариант 1:
# lst_address = session.query( Address ).all()
# for address in lst_address:
#     city = session.query(City).filter_by( id = address.id_city ).first()
#     region = session.query(Region).filter_by(id=address.id_region).first()
#     print(address.name, region.name, city.name, sep=', ' )
# Вариант 2:
query = session.query( Address, City, Region  )
# query = query.join( City, City.id == Address.id_city ).\
#     join( Region, Region.id == Address.id_region  )
query = query.join( City, City.id == Address.id_city        )
query = query.join( Region, Region.id == Address.id_region  )
records = query.all()
for address, city, reg in records:
    print( city, reg, address, sep='; ' )

print( '============  Характеристика =======================' )
# Вариант 1:
# lst_characteristic = session.query( Characteristic ).all()
# for ch in lst_characteristic:
#     address = session.query(Address).filter_by( id = ch.id_address ).first()
#     print(address.name, ch.data, sep=', ' )
# session.close()
# Вариант 2:
query = session.query( Characteristic, Address  )
query = query.join( Address, Address.id == Characteristic.id_address )

records = query.all()
for ch,address in records:
    print( address, ch, sep='; ' )
