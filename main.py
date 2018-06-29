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

            w = Weather10Day(country, city)

            textData = w.forecast10DaysText()
            moreweather.lblDay1Text.text = textData[0]
            moreweather.lblDay2Text.text = textData[1]
            moreweather.lblDay3Text.text = textData[2]
            moreweather.lblDay4Text.text = textData[3]
            moreweather.lblDay5Text.text = textData[4]
            moreweather.lblDay6Text.text = textData[5]
            moreweather.lblDay7Text.text = textData[6]
            moreweather.lblDay8Text.text = textData[7]
            moreweather.lblDay9Text.text = textData[8]
            moreweather.lblDay10Text.text = textData[9]

            highData = w.forecast10DaysHigh()
            moreweather.lblDay1High.text = highData[0] + "°C"
            moreweather.lblDay2High.text = highData[1] + "°C"
            moreweather.lblDay3High.text = highData[2] + "°C"
            moreweather.lblDay4High.text = highData[3] + "°C"
            moreweather.lblDay5High.text = highData[4] + "°C"
            moreweather.lblDay6High.text = highData[5] + "°C"
            moreweather.lblDay7High.text = highData[6] + "°C"
            moreweather.lblDay8High.text = highData[7] + "°C"
            moreweather.lblDay9High.text = highData[8] + "°C"
            moreweather.lblDay10High.text = highData[9] + "°C"

            lowData = w.forecast10DaysLow()
            moreweather.lblDay1Low.text = lowData[0] + "°C"
            moreweather.lblDay2Low.text = lowData[1] + "°C"
            moreweather.lblDay3Low.text = lowData[2] + "°C"
            moreweather.lblDay4Low.text = lowData[3] + "°C"
            moreweather.lblDay5Low.text = lowData[4] + "°C"
            moreweather.lblDay6Low.text = lowData[5] + "°C"
            moreweather.lblDay7Low.text = lowData[6] + "°C"
            moreweather.lblDay8Low.text = lowData[7] + "°C"
            moreweather.lblDay9Low.text = lowData[8] + "°C"
            moreweather.lblDay10Low.text = lowData[9] + "°C"

            days = w.dayList()
            moreweather.lblDay1Day.text = days[0]
            moreweather.lblDay2Day.text = days[1]
            moreweather.lblDay3Day.text = days[2]
            moreweather.lblDay4Day.text = days[3]
            moreweather.lblDay5Day.text = days[4]
            moreweather.lblDay6Day.text = days[5]
            moreweather.lblDay7Day.text = days[6]
            moreweather.lblDay8Day.text = days[7]
            moreweather.lblDay9Day.text = days[8]
            moreweather.lblDay10Day.text = days[9]

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
            lblun = Label(text=("Latest tweets from @" + un), size_hint_y=None)
            moretwitter.layoutMoreTwitter.add_widget(lblun)

            for i in range(9):
                lbltweet = Label(text=tweets[i], size_hint_y=None)
                lbltweet.texture_update()
                moretwitter.layoutMoreTwitter.add_widget(lbltweet)

            btnback = Button(text="Back", height=dp(40), size_hint_y=None, on_press=lambda a: self.back())
            moretwitter.layoutMoreTwitter.add_widget(btnback)
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
