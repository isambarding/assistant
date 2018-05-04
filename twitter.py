import requests
from requests_oauthlib import OAuth1

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

    # Gets the lastest tweet from a given username
    def userLatest(self, username):
        url = "https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=" + username + "&count=1"
        response = requests.get(url, auth=self.auth)
        f = response.json()
        q = f[0]
        return q["text"]

    # Gets the previous 10 tweets from a given username.
    def user10(self, username):
        url = "https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=" + username + "&count=10"
        response = requests.get(url, auth=self.auth)
        f = response.json()
        s = []
        for tweet in f:
            s.append(tweet["text"])
        return s


# Testing
t = Twitter()
un = input("Enter an @username: ")
print(t.user10(un))
