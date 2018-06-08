import sqlite3


class NotesRemindersAlarms:
    def __init__(self):
        pass

    def sortAll(self):
        pass

    def searchAll(self, ntype, value):
        with sqlite3.connect("UserData.db") as db:
            cursor = db.cursor()
            cursor.execute("select * from " + ntype + " where title like %" + value + "%")
            results = cursor.fetchall()
            return results

    def dictate(self):
        pass

    def createAll(self, ntype, title):
        with sqlite3.connect("UserData.db") as db:
            cursor = db.cursor()
            sql = "insert into " + ntype + " (Title) values " + title
            cursor.execute(sql)
            db.commit

    def viewAll(self):
        pass

    def editAll(self):
        pass

    def deleteAll(self, ntype, idno):
        with sqlite3.connect("UserData.db") as db:
            cursor = db.cursor()
            sql = "delete from " + ntype + " where ID=" + idno
            cursor.execute(sql)
            db.commit()

# Notes class


class Notes(NotesRemindersAlarms):
    def create(self, title, content):
        self.createAll("Notes", title)
        with sqlite3.connect("UserData.db") as db:
            cursor = db.cursor()
            sql = "insert into Notes (Content) values (" + content
            cursor.execute(sql)
            db.commit

    def mostRecent(self):
        pass

    def delete(self, noteid):
        self.deleteAll(self, "Notes", noteid)

# Reminders class


class Reminders(NotesRemindersAlarms):
    def create(self, title, content, time):
        self.createAll("Notes", title)
        with sqlite3.connect("UserData.db") as db:
            cursor = db.cursor()
            sql = "insert into Notes (Content, Time) values (" + content
            cursor.execute(sql)
            db.commit

    def mostRecent(self):
        pass

    def delete(self, noteid):
        self.deleteAll(self, "Reminders", noteid)

# Alarms class


class Alarms(NotesRemindersAlarms):
    def create(self):
        pass

    def mostRecent(self):
        pass

    def delete(self, noteid):
        #self.deleteAll(self, "Alarms", noteid)
        pass

