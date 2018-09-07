import sqlite3

# works, apparently
# Holds setup methods
# could be moved to main


class Setup:
    # Create table method
    def createTable(self, sql):
        with sqlite3.connect(dbName) as db:
            cursor = db.cursor()
            cursor.execute(sql)

    # Main setup method
    def startSetup(self, name, country, city):
        dbName = "UserData.db"

        # Create userinfo
        sql = "CREATE TABLE userInfo (Name text, Country text, City text, LastTwitterSearch text, primary key(Name))"
        self.createTable(dbName, sql)

        with sqlite3.connect("UserData.db") as db:
            cursor = db.cursor()
            sql = """INSERT INTO userInfo (Name, Country, City, LastTwitterSearch) VALUES ('""" + name + """', '""" + country + """', '""" + city + """', 'kedst')"""
            cursor.execute(sql)

        # Alarms table
        sql = """CREATE TABLE Alarms (AlarmID integer, Title text, Days text, Time time, Date float, Repeats boolean, primary key(AlarmID))"""
        self.createTable(sql)

        # Notes table
        sql = """CREATE TABLE Notes
                    (NoteID integer,
                    Title text,
                    Content text,
                    Date float,
                    primary key(NoteID))"""
        self.createTable(dbName, sql)

        # Reminders table
        sql = """CREATE TABLE Reminders
                    (ReminderID integer,
                    Title text,
                    Content text,
                    Days text,
                    Time time,
                    Date float,
                    Repeats boolean,
                    primary key(ReminderID))"""
        self.createTable(dbName, sql)


# Testing
c = Setup()
c.startSetup("jake", "france", "paris")
