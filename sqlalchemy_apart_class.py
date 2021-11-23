from sqlalchemy import Column, Integer, String, Float, create_engine,Table, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapper, sessionmaker, create_session

from database_setup import Base, View_apartment, Country, Region, City, Address, Characteristic

from sqlalchemy.orm import scoped_session
#from sqlalchemy.pool import NullPool

engine = create_engine('sqlite:///books-collection.db?check_same_thread=False')
Base.metadata.bind = engine
#Base = declarative_base()
#metadata = MetaData( bind=engine  )


DBSession = sessionmaker( bind=engine )
session = DBSession()

#session_factory = sessionmaker(bind=engine)
#Session = scoped_session(session_factory)
#session = Session()


class SQLAlchemy_apartment:
    @classmethod
    def get_field(self):
        #print('============ Поля просмотра =======================')
        lst_field = session.query(View_apartment).all()
        lst=[]
        for field in lst_field:
            #print(field.colname, field.coltitle, sep=', ')
            lst.append( {'npp':field.npp, 'name':field.colname, 'title':field.coltitle} )
        #print('***********************')
        #print(lst)
        lst = sorted(  lst, key=lambda x: x['npp']  )  # сортировка по порядку
        #print(lst)
        #print('***********************')
        return lst

    @classmethod
    def get_country(self):
        query = session.query(City, Country)
        query = query.join(City, City.id_country == Country.id)
        records = query.all()
        lst=[]
        dic = {}
        for city, country in records:
            #print(city, country, sep=', ')
            lst.append( {'city':city, 'country':country} )
        return lst

    @classmethod
    def get_region(self, name):
        reg = session.query(Region).filter( Region.name == name).first()
        t = type( reg )
        lst = [reg.id, reg.name, reg.id_city, reg.date]

        return lst

    @classmethod
    def get_data(self, region):
        reg = self.get_region( region )
        id_reg = reg[0]
        upd = reg[3]

        query = session.query( Characteristic, Address ).filter( Address.id_region == id_reg )
        query = query.join( Address, Address.id == Characteristic.id_address )
        records = query.all()
        for char, address in records:
            print( address, char,  sep='; ')
        return (records, upd)