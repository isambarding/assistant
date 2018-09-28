import sqlite3
import time
import datetime


# Notes class
class Notes:
    def __init__(self):
        self.db = sqlite3.connect("UserData.db")
        self.cursor = self.db.cursor()

    def create(self, title, content):
        date = time.time()
        sql = """insert into Notes (Title, Content, Date) values ('{}', '{}', {});""".format(title, content, date)
        self.cursor.execute(sql)
        self.db.commit()

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

    def search(self, searchterm):
        sql = """SELECT NoteID, Title, Content FROM Notes WHERE Content LIKE '%{}%'""".format(searchterm)
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return data

    def sort(self, type):
        sql = """SELECT NoteID, Title, Content FROM Notes ORDER BY {}""".format(type)
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return data


# Reminders class
class Reminders:
    def __init__(self):
        self.db = sqlite3.connect("UserData.db")
        self.cursor = self.db.cursor()

    def create(self, title, content, year, month, day, hour, minute, second):
        date = datetime.datetime(year, month, day, hour, minute, second)
        date = date.timestamp()
        sql = """insert into Reminders (Title, Content, Date) values ('{}', '{}', {});""".format(title, content, date)
        self.cursor.execute(sql)
        self.db.commit()

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

    def search(self, searchterm):
        sql = """SELECT ReminderID, Title, Content FROM Reminders WHERE Content LIKE '%{}%'""".format(searchterm)
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return data

    def sort(self, type):
        sql = """SELECT ReminderID, Title, Content FROM Reminders ORDER BY {}""".format(type)
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return data
