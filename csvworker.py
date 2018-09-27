import csv
import sqlite3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from encryption import Crypto


class csvworker:
    def __init__(self):
        self.db = sqlite3.connect("UserData.db")
        self.cursor = self.db.cursor()
        self.c = Crypto(False, 0)

    # Method - exportcsv
    # Parameters - idtype: string
    # Return - None
    # Purpose - Creates a csv file from the user's selected database table (notes or reminders)
    def exportcsv(self, idtype):
        file = open("output.csv", "w")
        writer = csv.writer(file)
        sql = """SELECT {}ID, Title, Content, Date FROM {}s ORDER BY Title""".format(idtype, idtype)
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        print(data)
        writer.writerow(["ID", "Title", "Content", "Date"])
        for i in range(len(data)):
            writer.writerow([data[i][0], self.c.decrypt(data[i][1]), self.c.decrypt(data[i][2]), data[i][3]])
        print("CSV created")

    # Method - email
    # Parameters - username: string, password: string, target: string
    # Return - None
    # Purpose - Sends an email with the exported csv file attached over gmail servers using the user's email and
    #           password, to a user defined target address
    def email(self, username, password, target):
        msg = MIMEMultipart()
        msg['From'] = username
        msg['To'] = target
        msg['Subject'] = "Assistant - Data output"
        body = "Attached is the output data in csv format, as created by Assistant"
        msg.attach(MIMEText(body, 'plain'))
        filename = "output.csv"
        attachment = open("output.csv", "rb")
        file = MIMEBase('application', 'octet-stream')
        file.set_payload(attachment.read())
        encoders.encode_base64(file)
        file.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        msg.attach(file)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(username, password)
        text = msg.as_string()
        server.sendmail(username, target, text)
        print("Email sent")
        server.quit()
