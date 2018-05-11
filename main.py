from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import StringProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from weather import Weather4Day, Weather10Day
import sqlite3


class HomeScreen(Screen):
    labelName = StringProperty()

    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        self.updateName()

    def updateName(self, *args):
        with sqlite3.connect("UserData.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT name FROM userInfo")
            username = cursor.fetchone()
        self.labelName = "Welcome, " + username[0] + "!"


class WeatherScreen(Screen):
    labelWeatherText = StringProperty()

    def __init__(self, **kwargs):
        super(WeatherScreen, self).__init__(**kwargs)
        self.getCurrentWeather()

    # works in theory
    def getCurrentWeather(self, *args):
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
        w = Weather4Day(country, city)
        self.labelWeatherText = w.forecastTodayText()


class MoreWeatherScreen(Screen):
    pass


class TwitterScreen(Screen):
    pass


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
