import sqlite3

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

from weather import Weather4Day, Weather10Day
from twitter import Twitter

# Make label height scale with number of lines
# Finish moreweather
# do moretwitter layout
# do nra layouts
# do nra functions
# clean up text = first letter caps on names and locations


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
    def __init__(self, **kwargs):
        super(MoreWeatherScreen, self).__init__(**kwargs)
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
        self.w = Weather10Day(country, city)
        self.getTextForecast()
        #self.getHighForecast()

    def getTextForecast(self, *args):
        data = self.w.forecast10DaysText()
        self.labelDay1Text = data[0]
        self.labelDay2Text = data[1]
        self.labelDay3Text = data[2]
        self.labelDay4Text = data[3]
        self.labelDay5Text = data[4]
        self.labelDay6Text = data[5]
        self.labelDay7Text = data[6]
        self.labelDay8Text = data[7]
        self.labelDay9Text = data[8]
        self.labelDay10Text = data[9]

    # FIX THIS
    def getHighForecast(self, *args):
        data = self.w.forecast10DaysHigh()
        self.labelDay1High = data[0] + "°C"
        self.labelDay2High = data[1] + "°C"
        self.labelDay3High = data[2] + "°C"
        self.labelDay4High = data[3] + "°C"
        self.labelDay5High = data[4] + "°C"
        self.labelDay6High = data[5] + "°C"
        self.labelDay7High = data[6] + "°C"
        self.labelDay8High = data[7] + "°C"
        self.labelDay9High = data[8] + "°C"
        self.labelDay10High = data[9] + "°C"


class TwitterScreen(Screen):
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

