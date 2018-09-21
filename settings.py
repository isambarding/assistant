# settings file: user changes name and location details
import sqlite3
from encryption import Crypto


class Settings:
    def __init__(self):
        self.db = sqlite3.connect("UserData.db")
        self.cursor = self.db.cursor()
        self.c = Crypto()

    def changeName(self, name):
        name = self.c.encrypt(name)
        self.cursor.execute("""UPDATE userInfo SET Name='{}'""".format(name))
        self.db.commit()

    def changeLocation(self, country, city):
        country = self.c.encrypt(country)
        city = self.c.encrypt(city)
        self.cursor.execute("""UPDATE userInfo SET Country='{}'""".format(country))
        self.cursor.execute("""UPDATE userInfo SET City='{}'""".format(city))
        self.db.commit()


class Setup:
    def __init__(self):
        self.db = sqlite3.connect("UserData.db")
        self.cursor = self.db.cursor()

    # Main setup method
    def completeSetup(self, name, country, city):
        c = Crypto(True, len(name))
        name = c.encrypt(name)
        country = c.encrypt(country)
        city = c.encrypt(city)
        un = c.encrypt("kedst")

        sql = "CREATE TABLE userInfo (Name text, Country text, City text, LastTwitterSearch text, primary key(Name))"
        self.cursor.execute(sql)

        sql = """INSERT INTO userInfo (Name, Country, City, LastTwitterSearch) VALUES ('{}', '{}', '{}', '{}')""".format(name, country, city, un)
        self.cursor.execute(sql)

        # Notes table
        sql = """CREATE TABLE Notes (NoteID integer, Title text, Content text, Date float, primary key(NoteID))"""
        self.cursor.execute(sql)

        # Reminders table
        sql = """CREATE TABLE Reminders (ReminderID integer, Title text, Content text, Days text, Time time, Date float, Repeats boolean, primary key(ReminderID))"""
        self.cursor.execute(sql)
        self.db.commit()
