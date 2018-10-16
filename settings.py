import sqlite3
from encryption import Crypto


class Settings:
    # Method - Settings init
    # Parameters - None
    # Return - None
    # Purpose - Initialises an instance of the crypto class for this class and sets up the database for editing
    def __init__(self):
        self.db = sqlite3.connect("UserData.db")
        self.cursor = self.db.cursor()
        self.c = Crypto(None, 0)

    # Method - changename
    # Parameters - name: string
    # Return - None
    # Purpose - Encrypts the user's chosen name then sets the user's name in the database
    def changename(self, name):
        name = self.c.encrypt(name)
        self.cursor.execute("""UPDATE userInfo SET Name='{}'""".format(name))
        self.db.commit()

    # Method - changelocation
    # Parameters - country: string, city: string
    # Return - None
    # Purpose - Sets the user's location in the database to the country and city arguments
    def changelocation(self, country, city):
        country = self.c.encrypt(country)
        city = self.c.encrypt(city)
        self.cursor.execute("""UPDATE userInfo SET Country='{}'""".format(country))
        self.cursor.execute("""UPDATE userInfo SET City='{}'""".format(city))
        self.db.commit()


class Setup:
    # Method - completesetup
    # Parameters - name: string, country: string, city: string
    # Return - None
    # Purpose - Creates the database ables and adds the user's information to the database
    def completesetup(self, name, country, city):
        c = Crypto(True, len(name))
        name = c.encrypt(name)
        country = c.encrypt(country)
        city = c.encrypt(city)
        un = c.encrypt("kedst")
        db = sqlite3.connect("UserData.db")
        cursor = db.cursor()

        sql = "CREATE TABLE userInfo (Name text, Country text, City text, LastTwitterSearch text, primary key(Name))"
        cursor.execute(sql)

        sql = """INSERT INTO userInfo (Name, Country, City, LastTwitterSearch) VALUES ('{}', '{}', '{}', '{}')""".format(name, country, city, un)
        cursor.execute(sql)

        # Notes table
        sql = """CREATE TABLE Notes (NoteID integer, Title text, Content text, Date float, primary key(NoteID))"""
        cursor.execute(sql)

        # Reminders table
        sql = """CREATE TABLE Reminders (ReminderID integer, Title text, Content text, Date float, primary key(ReminderID))"""
        cursor.execute(sql)
        db.commit()
