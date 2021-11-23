from sqlalchemy import Column, Integer, String, Float, create_engine,Table, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapper, sessionmaker, create_session

from sqlalchemy.orm import scoped_session
#from sqlalchemy.pool import NullPool

Base = declarative_base()

# class Country( Base ):
#     __tablename__ = 'Country'
#
#     id = Column( Integer, primary_key=True )
#     name = Column(String)
#
# class Region( Base ):
#     __tablename__ = 'Region'
#
#     id = Column( Integer, primary_key=True)
#     name = Column( String )
#     id_city = Column( Integer, ForeignKey( 'City.id' )  )
#     date = Column( String )
#
# class City( Base ):
#     __tablename__ = 'City'
#
#     id = Column( Integer, primary_key=True )
#     name = Column(String)
#     id_country = Column(Integer, ForeignKey('Country.id'))


engine = create_engine( 'sqlite:///apartment.db', echo=False )
#Base.metadata.create_all( engine )
metadata = MetaData( bind=engine  )


class View_apartment( Base ):
    __table__ = Table('View_apartment', metadata, autoload=True)

    def __init__(self, npp, colname, coltitle):
        self.npp = npp
        self.colname = colname
        self.coltitle = coltitle

    def __str__(self):
        return f'{self.coltitle}'


class Region(Base):
    __table__ = Table('Region', metadata, autoload=True)

    def __init__(self, name, id_city, date):
        self.name = name
        self.id_city = id_city
        self.date = date

    def __str__(self):
        return f'{self.name}'


class City(Base):
    __table__ = Table('City', metadata, autoload=True)

    def __init__(self, name, id_country):
        self.name = name
        self.id_country = id_country

    def __str__(self):
        return f'{self.name}'


class Country(Base):
    __table__ = Table('Country', metadata, autoload=True)

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f'{self.name}'


class Address(Base):
    __table__ = Table('Address', metadata, autoload=True)

    def __init__(self, id_region, id_city, name):
        self.id_region = id_region
        self.id_city = id_city
        self.name = name

    def __str__(self):
        return f'{self.name}'


class Characteristic(Base):
    __table__ = Table('Characteristic', metadata, autoload=True)

    def __init__(self, id_address, data):
        self.id_address = id_address
        self.data = data

    def __str__(self):
        return f'{self.data}'

