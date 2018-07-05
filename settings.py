# settings file: user changes name and location details
import sqlite3


class Settings:
    def __init__(self):
        self.db = sqlite3.connect("UserData.db")
        self.cursor = self.db.cursor()

    def changeName(self, name):
        self.cursor.execute("""UPDATE userInfo SET Name='{}'""".format(name))
        self.db.commit()

    def changeLocation(self, country, city):
        self.cursor.execute("""UPDATE userInfo SET Country='{}'""".format(country))
        self.cursor.execute("""UPDATE userInfo SET City='{}'""".format(city))
        self.db.commit()
