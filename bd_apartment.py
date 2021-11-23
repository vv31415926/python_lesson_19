import sqlite3 as lite
import datetime

class Appartment_BD:
    def __init__(self):
        self.NAMEBASE = 'apartment.db'
        self.connect=None
        self.cursor:lite = None
        self.is_connect = self.ini_connect()

    def ini_connect(self):
        r = 'OK'
        try:
            self.connect = lite.connect( self.NAMEBASE )
            self.cursor = self.connect.cursor()
        except lite.Error as e:
            r = e.args[0]
        return r

    def get_is_connect(self):
        return self.is_connect


    def get_title_table(self):
        sSQL = 'select colname, coltitle from view_apartment order by npp'
        self.cursor.execute( sSQL )
        r = self.cursor.fetchall()
        tt = type(r)
        for ri in r:
            print( ri[0], ri[1] )
        return r

    def save_data(self, lst:list): #
        s1 = lst[0]['region'].replace( ',',' ' )
        reg = ' '.join(  s1.split(' ')[0:2]  )
        id_reg = self.set_region( reg )

        for v in lst:
            id_addr = self.set_address( id_reg, v['address'] )
            id_charact = self.set_characteristic(id_addr, v['characteristic'])



    def set_region(self, name ):
        sSQL = f'SELECT * FROM region WHERE name="{name}" LIMIT 1'
        self.cursor.execute( sSQL )
        res = self.cursor.fetchone()  #[0]
        if not res:  # нет такого района
            today = datetime.datetime.today().strftime('%d-%m-%Y')  # .strftime('%d-%m-%Y')
            sSQL = 'insert into region VALUES (NULL,?,?,?)'
            self.cursor.execute( sSQL, [name, 1, today] )
            self.connect.commit()

            sSQL = f'SELECT id FROM region WHERE name="{name}" LIMIT 1'
            self.cursor.execute(sSQL)
            id = self.cursor.fetchone()[0]
        else:
            id = res[0]
        return  id

    def set_address(self, id_reg, name ):
        sSQL = f'SELECT * FROM address WHERE id_region={id_reg} and name="{name}" LIMIT 1'
        self.cursor.execute( sSQL )
        res = self.cursor.fetchone()  #[0]

        if not res:  # нет такого
            sSQL = 'insert into address VALUES (NULL,?,?,?)'
            self.cursor.execute( sSQL, [ name, 1, id_reg ] )
            self.connect.commit()

            sSQL = f'SELECT id FROM address WHERE id_region={id_reg} and name="{name}" LIMIT 1'
            self.cursor.execute(sSQL)
            aaa = self.cursor.fetchone()
            id = aaa[0]   #self.cursor.fetchone()[0]
        else:
            id = res[0]
        return id

    def set_characteristic(self, id_addr, data ):
        sSQL = f'SELECT * FROM characteristic WHERE id_address={id_addr} LIMIT 1'
        self.cursor.execute( sSQL )
        res = self.cursor.fetchone()  #[0]

        if not res:  # нет такого
            sSQL = 'insert into characteristic VALUES (NULL,?,?)'
            self.cursor.execute( sSQL, [ id_addr, data ] )
            self.connect.commit()

            sSQL = f'SELECT id FROM characteristic WHERE id_address={id_addr} LIMIT 1'
            self.cursor.execute(sSQL)
            id = self.cursor.fetchone()[0]
        else:
            id = res[0]
        return id

    def get_data(self, name_region ):
        sSQL = f'SELECT * FROM region WHERE name="{name_region}" LIMIT 1'
        self.cursor.execute(sSQL)
        res = self.cursor.fetchone()
        update = ' '
        if  res:
            id_reg = res[0]
            update = res[3]
            sSQL = f'SELECT a.name, c.data FROM address as a, characteristic as c WHERE a.id_city=1 and a.id_region={id_reg} and c.id_address=a.id'
            self.cursor.execute(sSQL)
            res = self.cursor.fetchall()
        else:
            res = []
        return (res,update)