import sqlite3


def create_table(dbName, sql):
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()


if __name__ == "__main__":
    dbName = "NotesRemindersAlarms.db"
    sql = """CREATE TABLE Alarms
            (AlarmID integer,
            Title text,
            Days text,
            Time time,
            CreationDate datetime,
            Repeats boolean,
            primary key(AlarmID))"""
    create_table(dbName, sql)


class NotesRemindersAlarms:
    def __init__(self):
        pass

    def sort:
        pass

    def search(self, nType, value):
        with sqlite3.connect("UserData.db") as db:
            cursor = db.cursor()
            cursor.execute("select * from " + nType + " where title like %" + value + "%")
            results = cursor.fetchall()
            return results

    def dictate:
        pass

    def create(self, ntype, title):
        with sqlite3.connect("UserData.db") as db:
            cursor = db.cursor()
            sql = "insert into " + ntype + " (Title) values " + title
            cursor.execute(sql, values)
            db.commit

    def viewAll:
        pass

    def edit:
        pass

    def delete(self, ntype, idno):
        with sqlite3.connect("UserData.db") as db:
            cursor = db.cursor()
            sql = "delete from " + ntype + " where ID=" + idno
            cursor.execute(sql, data)
            db.commit()


class notes(NotesRemindersAlarms):
    def delete(self, noteid):
        NotesRemindersAlarms.delete(self, "Notes", noteid)



