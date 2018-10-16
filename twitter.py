import requests
from requests_oauthlib import OAuth1


class Twitter:
    # Method - Twitter init
    # Parameters - token: string, appkey: string, appsecret: string, tokensecret: string
    # Return - Non
    # Purpose - Sets up and authorises a Twitter API request, ready to be called
    def __init__(self):
        token = "989416304108064770-HwtBl1mm13xiKBOMqlTjq2roq9SZCh0"
        appkey = "RcuKZbyWJiSXxsb57Pvuprkzr"
        appsecret = "CSdnGZ1ZZkPfMrWF9qTR98sRAFMPiuTf1OSouAHVOd8hCKHzmN"
        tokensecret = "pRhsJmMozHLycb7e6rc2wy0Xrk74e2yvVIZkfaGUYCFLU"
        self.auth = OAuth1(appkey, appsecret, token, tokensecret)
        self.twurl = "https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name="

    # Method - userlatest
    # Parameters - username: string
    # Return - text: string
    # Purpose - Gets the latest tweet from a given username from the Twitter API
    def userlatest(self, username):
        url = self.twurl + username + "&count=1"
        response = requests.get(url, auth=self.auth)
        f = response.json()
        try:
            q = f[0]
            return q["text"]
        except:
            return "No tweets found!"

    # Method - user10
    # Parameters - username: string
    # Return - s: string
    # Purpose - Gets the previous 10 tweets from a given username from the Twitter API
    def user10(self, username):
        url = self.twurl + username + "&count=10"
        response = requests.get(url, auth=self.auth)
        f = response.json()
        s = []
        for tweet in f:
            try:
                s.append(tweet["text"])
            except:
                s = ["No tweets found!"]
        return s

