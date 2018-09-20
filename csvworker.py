import csv
import sqlite3
from encryption import Crypto


class csvworker:
    def __init__(self):
        self.db = sqlite3.connect("UserData.db")
        self.cursor = self.db.cursor()
        self.c = Crypto(False, 0)

    def importcsv(self):
        pass
        #open file dialogue
        #parse file
        #turn file into notes etc

    def exportcsv(self, type):
        file = open("output.csv", "w")
        writer = csv.writer(file)
        sql = """SELECT {}ID, Title, Content, Date FROM {}s ORDER BY Title""".format(type, type)
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        count = len(data)

        writer.writerow(["ID", "Title", "Content", "Date"])
        for i in range(count):
            writer.writerow([data[i][0], self.c.decrypt(data[i][1]), self.c.decrypt(data[i][2]), data[i][3]])
