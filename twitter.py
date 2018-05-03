import requests
from requests_oauthlib import OAuth1

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
        return(q["text"])

    # not working
    def user10(self, username):
        url = "https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=" + username + "&count=10"
        response = requests.get(url, auth=self.auth)
        f = response.json()
        q = f[0]
        s=[]
        for tweet in q:
            s.append(q["text"])
        return(s)


#Testing
t = Twitter()
un = input("Enter an @username: ")
print(t.userLatest(un))
