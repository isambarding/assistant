# settings file: user changes name and location details
import sqlite3


class Settings:

    def changeName(self, name):
        with sqlite3.connect("UserData.db") as db:
            cursor = db.cursor()
            cursor.execute('UPDATE userInfo SET Name="' + name + '"')


    def changeLocation(self, country, city):
        with sqlite3.connect("UserData.db") as db:
            cursor = db.cursor()
            cursor.execute('UPDATE userInfo SET Country="' + country + '"')
            cursor.execute('UPDATE userInfo SET City="' + city + '"')