import sqlite3


class Crypto:
    def __init__(self, setup, length):
        self.alpha = "abcdefghijklmnopqrstuvwxyz"
        if setup is True:
            self.key = length

        else:
            with sqlite3.connect("UserData.db") as db:
                cursor = db.cursor()
                cursor.execute("SELECT Name FROM userInfo")
                name = cursor.fetchone()
            name = name[0]
            self.key = len(name)

    def encrypt(self, ciphertext):
        text = ""
        for c in ciphertext:
            if c in self.alpha:
                i = self.alpha.find(c)
                i = i + self.key
                if i > 25:
                    i = i - len(self.alpha)
                text = text + self.alpha[i]
            else:
                text = text + c
        return text

    def decrypt(self, ciphertext):
        text = ""
        for c in ciphertext:
            if c in self.alpha:
                i = self.alpha.find(c)
                i = i - self.key
                if i < 0:
                    i = i + len(self.alpha)
                text = text + self.alpha[i]
            else:
                text = text + c
        return text
