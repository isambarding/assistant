import sqlite3


class NotesRemindersAlarms:
    def __init__(self):
        self.db = sqlite3.connect("UserData.db")
        self.cursor = self.db.cursor()

    def searchAll(self, ntype, value):
        sql = """select * from {} where Title like '%{}%'""".format(ntype, value)
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        return results

    def dictate(self):
        pass

    def createAll(self, ntype, title):
        sql = """insert into {} (Title) values ('{}');""".format(ntype, title)
        self.cursor.execute(sql)
        self.db.commit()

    def viewAllChrono(self, ntype):
        self.cursor.execute("select Title from " + ntype + " order by dDate desc")
        results = self.cursor.fetchall()
        return results

    def viewAllAlpha(self, ntype):
        pass

    def editAll(self):
        pass

    def deleteAll(self, ntype, idno):
        sql = "delete from " + ntype + " where ID=" + idno
        self.cursor.execute(sql)
        self.db.commit()

# Notes class


class Notes(NotesRemindersAlarms):
    def create(self, title, content):
        self.createAll("Notes", title)
        sql = """insert into Notes (Content) values ('{}');""".format(content)
        self.cursor.execute(sql)
        self.db.commit()
        print("note created")

    def mostRecent(self):
        pass

    def delete(self, noteid):
        self.deleteAll("Notes", noteid)

# Reminders class


class Reminders(NotesRemindersAlarms):
    def create(self, title, content, time):
        self.createAll("Notes", title)
        sql = """insert into Reminders (Content, Time) values ('{}', '{}')""".format(content, time)
        self.cursor.execute(sql)
        self.db.commit()

    def mostRecent(self):
        pass

    def delete(self, noteid):
        self.deleteAll("Reminders", noteid)

# Alarms class


class Alarms(NotesRemindersAlarms):
    def create(self):
        pass

    def mostRecent(self):
        pass

    def delete(self, noteid):
        # self.deleteAll(self, "Alarms", noteid)
        pass

# testing
# n = Notes()
# t = input("Enter title")
# c = input("Enter content")
# n.create(t, c)
