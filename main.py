import sqlite3

from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen

from weather import Weather4Day, Weather10Day
from twitter import Twitter
from settings import Settings
from NotesRemindersAlarms import NotesRemindersAlarms, Notes, Reminders, Alarms
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.metrics import dp


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)

        with sqlite3.connect("UserData.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT name FROM userInfo")
            username = cursor.fetchone()

        self.lblName = "Welcome, " + username[0] + "!"


class WeatherScreen(Screen):
    latestWeatherText = StringProperty()
    latestWeatherHigh = StringProperty()
    latestWeatherLow = StringProperty()
    latestLocation = StringProperty()

    def __init__(self, **kwargs):
        super(WeatherScreen, self).__init__(**kwargs)
        self.getWeather()

    def getWeather(self):
        with sqlite3.connect("UserData.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT city FROM userInfo")
            city = cursor.fetchone()
            cursor.execute("SELECT country FROM userInfo")
            country = cursor.fetchone()
        city = city[0]
        country = country[0]

        w = Weather4Day(country, city)
        self.latestLocation = "The weather in {}, {} is:".format(city, country)
        self.latestWeatherText = w.forecastTodayText()
        self.latestWeatherHigh = w.forecastTodayHigh() + "°C"
        self.latestWeatherLow = w.forecastTodayLow() + "°C"

    def getMoreWeather(self):
        city = self.inputCity.text
        country = self.inputCountry.text
        
        if city == "" or country == "":
            pass
        else:
            moreweather = self.manager.get_screen("moreweather")
            moreweather.layoutMoreWeather.clear_widgets(moreweather.layoutMoreWeather.children)

            w = Weather10Day(country, city)
            textdata = w.forecast10DaysText()
            highdata = w.forecast10DaysHigh()
            lowdata = w.forecast10DaysLow()
            days = w.dayList()

            for i in range(9):
                lblday = Label(text=days[i], size_hint_y=None)
                lblday.texture_update()
                moreweather.layoutMoreWeather.add_widget(lblday)

                lbltext = Label(text=textdata[i], size_hint_y=None)
                lbltext.texture_update()
                moreweather.layoutMoreWeather.add_widget(lbltext)

                grid = GridLayout(cols=2, size_hint_y=None)
                lblhigh = Label(text=highdata[i], size_hint_y=None)
                lbllow = Label(text=lowdata[i], size_hint_y=None)
                lblhigh.texture_update()
                lbllow.texture_update()
                grid.add_widget(lblhigh)
                grid.add_widget(lbllow)
                moreweather.layoutMoreWeather.add_widget(grid)

            btnback = Button(text="Back", height=dp(40), size_hint_y=None, on_press=lambda a: self.back())
            moreweather.layoutMoreWeather.add_widget(btnback)
            self.manager.current = "moreweather"

    def back(self):
        self.manager.current = "weather"


class MoreWeatherScreen(Screen):
    def __init__(self, **kwargs):
        super(MoreWeatherScreen, self).__init__(**kwargs)


class TwitterScreen(Screen):
    recentTweet = StringProperty()
    recentUsername = StringProperty()

    def __init__(self, **kwargs):
        super(TwitterScreen, self).__init__(**kwargs)
        self.latestTweet()

    def latestTweet(self):
        with sqlite3.connect("UserData.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT LastTwitterSearch FROM userInfo")
            username = cursor.fetchone()

        username = username[0]
        t = Twitter()
        self.recentTweet = t.userLatest(username)
        self.recentUsername = "Latest tweet from @" + username

    def getMoreTweets(self):
        un = self.inputTwitterUsername.text
        if un == "":
            pass
        else:
            moretwitter = self.manager.get_screen("moretwitter")
            moretwitter.layoutMoreTwitter.clear_widgets(moretwitter.layoutMoreTwitter.children)

            t = Twitter()
            tweets = t.user10(un)
            lblun = Label(text=("Latest tweets from @" + un), size_hint_y=None)
            moretwitter.layoutMoreTwitter.add_widget(lblun)

            for i in range(9):
                lbltweet = Label(text=tweets[i], size_hint_y=None)
                lbltweet.texture_update()
                moretwitter.layoutMoreTwitter.add_widget(lbltweet)

            btnback = Button(text="Back", height=dp(40), size_hint_y=None, on_press=lambda a: self.back())
            moretwitter.layoutMoreTwitter.add_widget(btnback)
            self.parent.current = "moretwitter"

    def back(self):
        self.manager.current = "twitter"


class MoreTwitterScreen(Screen):
    def __init__(self, **kwargs):
        super(MoreTwitterScreen, self).__init__(**kwargs)

    def refreshTwitter(self):
        twitter = self.manager.get_screen("twitter")
        username = twitter.inputTwitterUsername.text

        with sqlite3.connect("UserData.db") as db:
            cursor = db.cursor()
            sql = """UPDATE userInfo SET LastTwitterSearch='{}'""".format(username)
            cursor.execute(sql)
            db.commit()

        t = Twitter()
        twitter.recentUsername = "Latest tweet from @" + username
        twitter.recentTweet = t.userLatest(username)
        self.parent.current = "twitter"


class NotesScreen(Screen):
    def __init__(self, **kwargs):
        super(NotesScreen, self).__init__(**kwargs)

    def newNote(self):
        self.parent.current = "newnotes"

    def notesByTime(self):
        morenotes = self.manager.get_screen("morenotes")
        morenotes.layoutMoreNotes.clear_widgets(morenotes.layoutMoreNotes.children)

        with sqlite3.connect("UserData.db") as db:
            cursor = db.cursor()
            sql = """SELECT NoteID, Title, Content FROM Notes ORDER BY Date"""
            cursor.execute(sql)
            data = cursor.fetchall()
            sql = """SELECT Count(NoteID) FROM Notes"""
            cursor.execute(sql)
            count = cursor.fetchall()
            count = count[0][0]

        for i in range(count):
            noteid = data[i][0]
            title = data[i][1]
            content = data[i][2]

            lbltitle = Label(text=title, size_hint_y=None)
            lbltitle.texture_update()
            morenotes.layoutMoreNotes.add_widget(lbltitle)

            lbltext = Label(text=content, size_hint_y=None)
            lbltext.texture_update()
            morenotes.layoutMoreNotes.add_widget(lbltext)

            grid = GridLayout(cols=2, size_hint_y=None)
            btnedit = Button(text="Edit", size_hint_y=None, on_press=lambda a: self.edit(noteid))
            btndelete = Button(text="Delete", size_hint_y=None, on_press=lambda a: self.delete(noteid))
            btnedit.texture_update()
            btndelete.texture_update()
            grid.add_widget(btnedit)
            grid.add_widget(btndelete)
            morenotes.layoutMoreNotes.add_widget(grid)

        morenotes.layoutMoreNotes.add_widget(Button(text="Back", height=dp(40), on_press=lambda a: self.back()))
        self.manager.current = "morenotes"

    def notesByTitle(self):
        self.manager.current = "morenotes"

    def back(self):
        self.manager.current = "notes"

    def delete(self, noteid):
        n = Notes()
        n.delete(noteid)
        self.manager.current = "notes"
        print("Note deleted")

    def edit(self, noteid):
        self.manager.current = "editnotes"


class NewNotesScreen(Screen):
    def __init__(self, **kwargs):
        super(NewNotesScreen, self).__init__(**kwargs)

    def createNote(self):
        title = self.inputNewNoteTitle.text
        content = self.inputNewNoteContent.text

        with sqlite3.connect("UserData.db") as db:
            cursor = db.cursor()
            sql = """SELECT Count(NoteID) FROM Notes"""
            cursor.execute(sql)
            count = cursor.fetchall()
            count = count[0][0]

        if title == "" or content == "":
            pass
        else:
            n = Notes()
            n.create(title, content)
            self.parent.current = "notes"


class MoreNotesScreen(Screen):
    pass


class EditNotesScreen(Screen):
    pass


class RemindersScreen(Screen):
    pass


class AlarmsScreen(Screen):
    pass


class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)

    def changeName(self):
        name = self.inputNewName.text
        if name == "":
            pass
        else:
            s = Settings()
            s.changeName(name)

    def changeLocation(self):
        city = self.inputNewCity.text
        country = self.inputNewCountry.text
        if city == "" or country == "":
            pass
        else:
            s = Settings()
            s.changeLocation(country, city)

    def restartSetup(self):
        pass


class MyScreenManager(ScreenManager):
    pass


class AssistantApp(App):
    def b(self):
        self.title = 'Assistant'


if __name__ == "__main__":
    app = AssistantApp()
    Window.size = (360, 640)
    app.run()
