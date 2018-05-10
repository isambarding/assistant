from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import StringProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
import sqlite3

# TODO fix name label: figure out how to access child widgets

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        with sqlite3.connect("UserData.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT name FROM userInfo")
            self.username = cursor.fetchone()
        self.username = self.username[0]
        # NOW BROKEN: commented for demo
        #self.children.labelName.text = "Welcome, " + self.username + "!"


class WeatherScreen(Screen):
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
