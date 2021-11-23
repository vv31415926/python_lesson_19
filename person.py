class Person:
    def __init__(self):
        self.name = 'Ива́н IV'
        self.otch = 'Васи́льевич'
        self.fam = 'Рюрикович'
        self.birthday = '25 августа 1530'
        self.prof ='государь, великий князь московский и всея Руси'
        self.photo = 'IvanIV.png'
        self.attached = ['Астрахань','Казань','Полоцк']

    def get_name(self):
        return self.name

    def get_otch(self):
        return self.otch

    def get_fam(self):
        return self.fam

    def get_birthday(self):
        return self.birthday

    def get_photo(self):
        return self.photo

    def get_attach(self):
        return self.attached


if __name__ == "__main__":
    p = Person()
    ph = p.get_photo()