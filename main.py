import sqlite3

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen

from weather import Weather4Day, Weather10Day
from twitter import Twitter

# Make label height scale with number of lines
# moreweather custom forecast
# do moretwitter layout
# do nra layouts
# do nra functions
# clean up text = first letter caps on names and locations


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)

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
            cursor.execute("SELECT country FROM userInfo")
            country = cursor.fetchone()
        city = city[0]
        country = country[0]

        w = Weather4Day(country, city)
        self.labelLocation = "The weather in " + city + ", " + country + " is:"
        self.labelWeatherText = w.forecastTodayText()
        self.labelWeatherHigh = w.forecastTodayHigh() + "°C"
        self.labelWeatherLow = w.forecastTodayLow() + "°C"
        self.inputCountry = country
        self.inputCity = city

        #def change_text(self):
        #    self.text = "The text you want to set"
        #    self.manager.current = "MoreWeatherScreen"


class MoreWeatherScreen(Screen):
    def __init__(self, **kwargs):
        super(MoreWeatherScreen, self).__init__(**kwargs)

        #with sqlite3.connect("UserData.db") as db:
        #    cursor = db.cursor()
        #    cursor.execute("SELECT city FROM userInfo")
        #    city = cursor.fetchone()
        #    cursor.execute("SELECT country FROM userInfo")
        #    country = cursor.fetchone()
        #city = city[0]
        #country = country[0]

        country = WeatherScreen.inputCountry
        city = WeatherScreen.inputCity

        w = Weather10Day(country, city)

        textData = w.forecast10DaysText()
        self.labelDay1Text = textData[0]
        self.labelDay2Text = textData[1]
        self.labelDay3Text = textData[2]
        self.labelDay4Text = textData[3]
        self.labelDay5Text = textData[4]
        self.labelDay6Text = textData[5]
        self.labelDay7Text = textData[6]
        self.labelDay8Text = textData[7]
        self.labelDay9Text = textData[8]
        self.labelDay10Text = textData[9]

        highData = w.forecast10DaysHigh()
        self.labelDay1High = highData[0] + "°C"
        self.labelDay2High = highData[1] + "°C"
        self.labelDay3High = highData[2] + "°C"
        self.labelDay4High = highData[3] + "°C"
        self.labelDay5High = highData[4] + "°C"
        self.labelDay6High = highData[5] + "°C"
        self.labelDay7High = highData[6] + "°C"
        self.labelDay8High = highData[7] + "°C"
        self.labelDay9High = highData[8] + "°C"
        self.labelDay10High = highData[9] + "°C"
        
        lowData = w.forecast10DaysLow()
        self.labelDay1Low = lowData[0] + "°C"
        self.labelDay2Low = lowData[1] + "°C"
        self.labelDay3Low = lowData[2] + "°C"
        self.labelDay4Low = lowData[3] + "°C"
        self.labelDay5Low = lowData[4] + "°C"
        self.labelDay6Low = lowData[5] + "°C"
        self.labelDay7Low = lowData[6] + "°C"
        self.labelDay8Low = lowData[7] + "°C"
        self.labelDay9Low = lowData[8] + "°C"
        self.labelDay10Low = lowData[9] + "°C"

        days = w.dayList()
        self.labelDay1Day = days[0]
        self.labelDay2Day = days[1]
        self.labelDay3Day = days[2]
        self.labelDay4Day = days[3]
        self.labelDay5Day = days[4]
        self.labelDay6Day = days[5]
        self.labelDay7Day = days[6]
        self.labelDay8Day = days[7]
        self.labelDay9Day = days[8]
        self.labelDay10Day = days[9]


class TwitterScreen(Screen):
    def __init__(self, **kwargs):
        super(TwitterScreen, self).__init__(**kwargs)

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


class AssistantApp(App):
    def b(self):
        self.title = 'Assistant'


if __name__ == "__main__":
    app = AssistantApp()
    app.run()
