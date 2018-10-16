import sqlite3
import time
import datetime


# Notes class
class Notes:
    def __init__(self):
        self.db = sqlite3.connect("UserData.db")
        self.cursor = self.db.cursor()

    # Method - create
    # Parameters - title: string, content: string
    # Return - None
    # Purpose - Inserts the title, content, and current datetime into the database
    def create(self, title, content):
        date = time.time()
        sql = """insert into Notes (Title, Content, Date) values ('{}', '{}', {});""".format(title, content, date)
        self.cursor.execute(sql)
        self.db.commit()

    # Method - mostrecent
    # Parameters - None
    # Return - data: list of strings
    # Purpose - Fetches the most recently created note from the database
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

    # Method - delete
    # Parameters - noteid: integer
    # Return - None
    # Purpose - Deletes the note corresponding to the given noteid
    def delete(self, noteid):
        sql = """delete from Notes where NoteID='{}'""".format(noteid)
        self.cursor.execute(sql)
        self.db.commit()

    # Method - edit
    # Parameters - noteid: integer, title: string, content: string
    # Return - None
    # Purpose - Edits the note corresponding to the given noteid, replacing the current values with those in title and
    #           content
    def edit(self, noteid, title, content):
        sql = """UPDATE Notes SET Title='{}', Content='{}' WHERE NoteID='{}';""".format(title, content, noteid)
        self.cursor.execute(sql)
        self.db.commit()

    # Method - search
    # Parameters - searchterm: string
    # Return - data: list of strings
    # Purpose - Returns the notes that have the search term in their title
    def search(self, searchterm):
        sql = """SELECT NoteID, Title, Content FROM Notes WHERE Content LIKE '%{}%'""".format(searchterm)
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return data

    # Method - sort
    # Parameters - type: string
    # Return - data: list of strings
    # Purpose - Returns the user's notes, sorted by the given sort type (alphabetical or by date)
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

    # Method - create
    # Parameters - title: string, content: string, year: integer, month: integer, day: integer, hour: integer,
    #              minute: integer, second: integer
    # Return - None
    # Purpose - Inserts the title, content, and given datetime into the database
    def create(self, title, content, year, month, day, hour, minute, second):
        date = datetime.datetime(year, month, day, hour, minute, second)
        date = date.timestamp()
        sql = """insert into Reminders (Title, Content, Date) values ('{}', '{}', {});""".format(title, content, date)
        self.cursor.execute(sql)
        self.db.commit()

    # Method - mostrecent
    # Parameters - None
    # Return - data: list of strings
    # Purpose - Fetches the next reminder from the database
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

    # Method - delete
    # Parameters - reminderid: integer
    # Return - None
    # Purpose - Deletes the reminder corresponding to the given reminderid
    def delete(self, reminderid):
        sql = """delete from Reminders where ReminderID='{}'""".format(reminderid)
        self.cursor.execute(sql)
        self.db.commit()

    # Method - edit
    # Parameters - reminderid: integer, title: string, content: string
    # Return - None
    # Purpose - Edits the reminder corresponding to the given reminderid, replacing the current values with those in
    #           title and content
    def edit(self, reminderid, title, content):
        sql = """UPDATE Reminders SET Title='{}', Content='{}' WHERE ReminderID='{}';""".format(title, content, reminderid)
        self.cursor.execute(sql)
        self.db.commit()

    # Method - search
    # Parameters - searchterm: string
    # Return - data: list of strings
    # Purpose - Returns the reminders that have the search term in their title
    def search(self, searchterm):
        sql = """SELECT ReminderID, Title, Content, Date FROM Reminders WHERE Content LIKE '%{}%'""".format(searchterm)
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return data

    # Method - sort
    # Parameters - type: string
    # Return - data: list of strings
    # Purpose - Returns the user's reminders, sorted by the given sort type (alphabetical or by date)
    def sort(self, type):
        sql = """SELECT ReminderID, Title, Content, Date FROM Reminders ORDER BY {}""".format(type)
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return data
