import sqlite3


class Crypto:
    # Method - Crypto init
    # Parameters - setup: boolean, length: integer
    # Return - None
    # Purpose - Determines if the program is in setup mode, if not then the key is the length of the user's name in the
    #           database, if it is then the key is the length argument
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

    # Method - encrypt
    # Parameters - ciphertext: string
    # Return - text: string
    # Purpose - Encrypts the given ciphertext with a simple caesar cipher
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

    # Method - decrypt
    # Parameters - ciphertext: string
    # Return - text: string
    # Purpose - Decrypts the given ciphertext with a simple caesar cipher
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
