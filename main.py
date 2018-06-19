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
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.metrics import dp

# do moretwitter layout - dates etc

# do nra layouts
# do nra functions

# Make lbl height scale with number of lines
# clean up user input = first letter caps on names and locations
# clean code
# error trapping!!!


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

            w = Weather10Day(country, city)
            textData = w.forecast10DaysText()
            highData = w.forecast10DaysHigh()
            lowData = w.forecast10DaysLow()
            days = w.dayList()

            for i in range(9):
                day = days[i]
                forecast = textData[i]
                high = highData[i]
                low = lowData[i]

                gridlayout = GridLayout(cols=2)
                moreweather.layoutMoreWeather.add_widget(Label(text=day))
                moreweather.layoutMoreWeather.add_widget(Label(text=forecast))
                moreweather.layoutMoreWeather.add_widget(gridlayout)
                gridlayout.add_widget(Label(text="High"))
                gridlayout.add_widget(Label(text=high))
                gridlayout.add_widget(Label(text="Low"))
                gridlayout.add_widget(Label(text=low))
            moreweather.layoutMoreWeather.add_widget(Button(text="Back", on_press=lambda a: self.back()))

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
            t = Twitter()
            tweets = t.user10(un)
            moretwitter.lblTwitterUsername.text = "Latest tweets from @" + un
            moretwitter.lblTweet1.text = tweets[0]
            moretwitter.lblTweet2.text = tweets[1]
            moretwitter.lblTweet3.text = tweets[2]
            moretwitter.lblTweet4.text = tweets[3]
            moretwitter.lblTweet5.text = tweets[4]
            moretwitter.lblTweet6.text = tweets[5]
            moretwitter.lblTweet7.text = tweets[6]
            moretwitter.lblTweet8.text = tweets[7]
            moretwitter.lblTweet9.text = tweets[8]
            moretwitter.lblTweet10.text = tweets[9]
            self.parent.current = "moretwitter"


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

        with sqlite3.connect("UserData.db") as db:
            cursor = db.cursor()
            sql = """SELECT NoteID, Title, Content FROM Notes ORDER BY Date"""
            cursor.execute(sql)
            data = cursor.fetchall()
            sql = """SELECT Count(NoteID) FROM Notes"""
            cursor.execute(sql)
            count = cursor.fetchall()
            count = count[0][0]
            print(data)

        for i in range(count):
            noteid = data[i][0]
            title = data[i][1]
            content = data[i][2]

            gridlayout = GridLayout(cols=2)
            morenotes.layoutMoreNotes.add_widget(Label(text=title))
            morenotes.layoutMoreNotes.add_widget(Label(text=content))
            morenotes.layoutMoreNotes.add_widget(gridlayout)
            gridlayout.add_widget(Button(text="Edit"))
            gridlayout.add_widget(Button(text="Delete"))
        morenotes.layoutMoreNotes.add_widget(Button(text="Back", on_press=lambda a: self.back()))

        self.parent.current = "morenotes"

    def notesByTitle(self):
        self.parent.current = "morenotes"

    def back(self):
        self.manager.current = "notes"


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

        if title == "" or content == "" or count >= 10:
            pass
        elif count < 10:
            n = Notes()
            n.create(title, content)
            self.parent.current = "notes"


class MoreNotesScreen(Screen):
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
