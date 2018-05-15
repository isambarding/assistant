import sqlite3

# complete this

class NotesRemindersAlarms:
    def __init__(self):
        pass

    def sort(self):
        pass

    def search(self, ntype, value):
        with sqlite3.connect("UserData.db") as db:
            cursor = db.cursor()
            cursor.execute("select * from " + ntype + " where title like %" + value + "%")
            results = cursor.fetchall()
            return results

    def dictate(self):
        pass

    def create(self, ntype, title):
        with sqlite3.connect("UserData.db") as db:
            cursor = db.cursor()
            sql = "insert into " + ntype + " (Title) values " + title
            cursor.execute(sql)
            db.commit

    def viewAll(self):
        pass

    def edit(self):
        pass

    def delete(self, ntype, idno):
        with sqlite3.connect("UserData.db") as db:
            cursor = db.cursor()
            sql = "delete from " + ntype + " where ID=" + idno
            cursor.execute(sql, idno)
            db.commit()


class Notes(NotesRemindersAlarms):
    # Notes class
    def create(self):
        pass

    def mostRecent(self):
        pass

    def delete(self, noteid):
        NotesRemindersAlarms.delete(self, "Notes", noteid)


class Reminders(NotesRemindersAlarms):
    # Notes class
    def create(self):
        pass

    def mostRecent(self):
        pass

    def delete(self, noteid):
        NotesRemindersAlarms.delete(self, "Reminders", noteid)


class Alarms(NotesRemindersAlarms):
    # Notes class
    def create(self):
        pass

    def mostRecent(self):
        pass

    def delete(self, noteid):
        NotesRemindersAlarms.delete(self, "Alarms", noteid)

