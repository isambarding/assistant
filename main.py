import sqlite3

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen

from weather import Weather4Day
from twitter import Twitter


class HomeScreen(Screen):

    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        self.updateName()

    def updateName(self, *args):
        #labelName = StringProperty()
        with sqlite3.connect("UserData.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT name FROM userInfo")
            username = cursor.fetchone()

        self.labelName = "Welcome, " + username[0] + "!"


class WeatherScreen(Screen):
    #labelWeatherText = StringProperty()

    def __init__(self, **kwargs):
        super(WeatherScreen, self).__init__(**kwargs)

        with sqlite3.connect("UserData.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT city FROM userInfo")
            city = cursor.fetchone()
        city = city[0]

        with sqlite3.connect("UserData.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT country FROM userInfo")
            country = cursor.fetchone()
        country = country[0]

        self.w = Weather4Day(country, city)
        self.getCurrentWeather()
        self.getCurrentHigh()
        self.getCurrentLow()
        self.getLocation(city, country)

    def getLocation(self, city, country, *args):
        self.labelLocation = "The weather in " + city + ", " + country + " is:"

    def getCurrentWeather(self, *args):
        self.labelWeatherText = self.w.forecastTodayText()

    def getCurrentHigh(self, *args):
        self.labelWeatherHigh = self.w.forecastTodayHigh() + "°C"

    def getCurrentLow(self, *args):
        self.labelWeatherLow = self.w.forecastTodayLow() + "°C"


class MoreWeatherScreen(Screen):
    pass


class TwitterScreen(Screen):
    #labelRecentTweet = StringProperty()

    def __init__(self, **kwargs):
        super(TwitterScreen, self).__init__(**kwargs)
        self.getLastTweet()

    def getLastTweet(self, *args):
        with sqlite3.connect("UserData.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT LastTwitterSearch FROM userInfo")
            username = cursor.fetchone()
        username = username[0]
        t = Twitter()
        self.labelRecentTweet = t.userLatest(username)


class NotesScreen(Screen):
    pass


class RemindersScreen(Screen):
    pass


class AlarmsScreen(Screen):
    pass


class SettingsScreen(Screen):
    pass


class MyScreenManager(ScreenManager):
    pass


presentation = Builder.load_file("assistant.kv")


class AssistantApp(App):
    def build(self):
        self.title = 'Assistant'
        return presentation


if __name__ == "__main__":
    app = AssistantApp()
    app.run()

