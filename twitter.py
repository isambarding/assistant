import requests
from requests_oauthlib import OAuth1
import sqlite3

# 04/05/18: tested working

# Class hold all methods related to the Twitter section
# Note that the API does not support Twitter's new 280 character tweets, so they are shortened.


class Twitter:
    def __init__(self):
        token = "989416304108064770-HwtBl1mm13xiKBOMqlTjq2roq9SZCh0"
        appkey = "RcuKZbyWJiSXxsb57Pvuprkzr"
        appsecret = "CSdnGZ1ZZkPfMrWF9qTR98sRAFMPiuTf1OSouAHVOd8hCKHzmN"
        tokensecret = "pRhsJmMozHLycb7e6rc2wy0Xrk74e2yvVIZkfaGUYCFLU"
        self.auth = OAuth1(appkey, appsecret, token, tokensecret)
        self.twurl = "https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name="

    # Gets the latest tweet from a given username
    def userLatest(self, username):
        url = self.twurl + username + "&count=1"
        response = requests.get(url, auth=self.auth)
        f = response.json()
        q = f[0]
        return q["text"]

    # Gets the previous 10 tweets from a given username.
    def user10(self, username):
        url = self.twurl + username + "&count=10"
        response = requests.get(url, auth=self.auth)
        f = response.json()
        s = []
        for tweet in f:
            s.append(tweet["text"])
        return s

    def updateUser(self, username):
        with sqlite3.connect("UserData.db") as db:
            cursor = db.cursor()
            sql = """UPDATE userInfo SET LastTwitterSearch='{}'""".format(username)
            cursor.execute(sql)
            db.commit()
        print("Last user search updated")

    def initUserLatest(self, userLatest):
        pass


# Testing
# t = Twitter()
# un = input("Enter an @username: ")
# print(t.userLatest(un))
