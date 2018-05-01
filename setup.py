import sqlite3

def create_table(dbName,sql):
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

