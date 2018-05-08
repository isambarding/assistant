from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import StringProperty
import sqlite3

# use screenmanager for screens


class HomeScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        with sqlite3.connect("UserData.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT name FROM userInfo")
            self.username = cursor.fetchone()
        self.username = self.username[0]
        print(self.username)
        self.namelabel.text = "Welcome, " + self.username + "!"


class AssistantApp(App):
    def build(self):
        self.title = 'Assistant'
        return HomeScreen()


if __name__ == "__main__":
    app = AssistantApp()
    app.run()
