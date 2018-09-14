import sqlite3
import time


class NotesRemindersAlarms:
    def __init__(self):
        self.db = sqlite3.connect("UserData.db")
        self.cursor = self.db.cursor()

    def searchAll(self, ntype, value):
        sql = """SELECT * FROM {} WHERE Title LIKE '%{}%'""".format(ntype, value)
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        return results

    def dictate(self):
        pass

    def createAll(self, ntype, title):
        pass
        # sql = """insert into {} (Title) values ('{}');""".format(ntype, title)
        # self.cursor.execute(sql)
        # self.db.commit()

    def viewAllChrono(self, ntype):
        sql = "SELECT Title FROM {} ORDER BY Date desc".format(ntype)
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        return results

    def viewAllAlpha(self, ntype):
        pass

    def editAll(self):
        pass

    def deleteAll(self, ntype, idno):
        pass

# Notes class


class Notes(NotesRemindersAlarms):
    def create(self, title, content):
        date = time.time()
        sql = """insert into Notes (Title, Content, Date) values ('{}', '{}', {});""".format(title, content, date)
        self.cursor.execute(sql)
        self.db.commit()
        print("Note created")

    def mostrecent(self):
        sql = """SELECT Max(Date) FROM Notes"""
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        data = data[0][0]
        sql = """SELECT Title, Content FROM Notes WHERE Date='{}'""".format(data)
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        if data:
            return data[0]
        else:
            return False

    def delete(self, noteid):
        sql = """delete from Notes where NoteID='{}'""".format(noteid)
        self.cursor.execute(sql)
        self.db.commit()

    def edit(self, noteid, title, content):
        sql = """UPDATE Notes SET Title='{}', Content='{}' WHERE NoteID='{}';""".format(title, content, noteid)
        self.cursor.execute(sql)
        self.db.commit()

# Reminders class


class Reminders(NotesRemindersAlarms):
    def create(self, title, content):
        date = time.time()
        sql = """insert into Reminders (Title, Content, Date) values ('{}', '{}', {});""".format(title, content, date)
        self.cursor.execute(sql)
        self.db.commit()
        print("Reminder created")

    def mostrecent(self):
        sql = """SELECT Max(Date) FROM Reminders"""
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        data = data[0][0]
        sql = """SELECT Title, Content FROM Reminders WHERE Date='{}'""".format(data)
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        if data:
            return data[0]
        else:
            return False

    def delete(self, reminderid):
        sql = """delete from Reminders where ReminderID='{}'""".format(reminderid)
        self.cursor.execute(sql)
        self.db.commit()

    def edit(self, reminderid, title, content):
        sql = """UPDATE Reminders SET Title='{}', Content='{}' WHERE ReminderID='{}';""".format(title, content, reminderid)
        self.cursor.execute(sql)
        self.db.commit()

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
