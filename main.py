# -*- coding: utf-8 -*-

import sqlite3
import os.path
import datetime

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

from weather import Weather4Day, Weather10Day
from settings import Setup, Settings
from twitter import Twitter
from encryption import Crypto
from csvworker import csvworker
from NotesReminders import Notes, Reminders

from kivy.core.window import Window
from kivy.uix.label import Label 
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.metrics import dp

# Assistant.txt contains layout, widget and formatting information for all of the screens
Builder.load_file("assistant.txt")

# Method -
# Parameters -
# Return -
# Purpose -

# Class HomeScreen contains code that will be run from within the "home" screen
class HomeScreen(Screen):
    # Method - HomeScreen init
    # Parameters - username: string
    # Return - None
    # Purpose - Retrieves the user's name from the database and displays it in a label when the screen is built by kivy
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)

        with sqlite3.connect("UserData.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT Name FROM userInfo")
            username = cursor.fetchone()
        c = Crypto(False, 0)
        username = c.decrypt(username[0])
        self.lblName.text = "Welcome, {}!".format(username)

########################################################################################################################


class WeatherScreen(Screen):
    # Method - WeatherScreen init
    # Parameters - None
    # Return - None
    # Purpose - Calls getweather function when the screen is built by kivy
    def __init__(self, **kwargs):
        super(WeatherScreen, self).__init__(**kwargs)
        self.getweather()

    # Method - getweather
    # Parameters - city: string, country: string
    # Return - None
    # Purpose - Gets the weather forecast for the current day for the user's set location and displays them in labels
    def getweather(self):
        with sqlite3.connect("UserData.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT city FROM userInfo")
            city = cursor.fetchone()
            cursor.execute("SELECT country FROM userInfo")
            country = cursor.fetchone()
        c = Crypto(False, 0)
        city = c.decrypt(city[0])
        country = c.decrypt(country[0])

        w = Weather4Day(country, city)

        self.lblLocation.text = "The weather in {}, {} is".format(city, country)
        self.lblWeatherText.text = w.forecasttodaytext()
        self.lblWeatherHigh.text = w.forecasttodayhigh() + "C"
        self.lblWeatherLow.text = w.forecasttodaylow() + "C"

    # Method - getmoreweather
    # Parameters - city: string, country: string, textdata: string, highdata: string, lowdata: string
    #              days: list of strings
    # Return - None
    # Purpose - Obtains and displays the data on the moreweather screen using the user's chosen location
    def getmoreweather(self):
        city = self.inputCity.text
        country = self.inputCountry.text
        
        if city == "" or country == "":
            pass
        else:
            moreweather = self.manager.get_screen("moreweather")
            moreweather.layoutMoreWeather.clear_widgets(moreweather.layoutMoreWeather.children)

            w = Weather10Day(country, city)
            textdata = w.forecast10daystext()
            highdata = w.forecast10dayshigh()
            lowdata = w.forecast10dayslow()
            days = w.daylist()

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

    # Method - back
    # Parameters - None
    # Return - None
    # Purpose - Displays the weather screen
    def back(self):
        self.manager.current = "weather"


class MoreWeatherScreen(Screen):
    def __init__(self, **kwargs):
        super(MoreWeatherScreen, self).__init__(**kwargs)

########################################################################################################################


class TwitterScreen(Screen):

    # Method - TwitterScreen init
    # Parameters - None
    # Return - None
    # Purpose - When kivy has built the screen, initialises instances of the Crypto and Twitter classes for this class,
    #           then calls the latesttweet function
    def __init__(self, **kwargs):
        super(TwitterScreen, self).__init__(**kwargs)
        self.db = sqlite3.connect("UserData.db")
        self.cursor = self.db.cursor()
        self.c = Crypto(False, 0)
        self.t = Twitter()
        self.latesttweet()

    # Method - latesttweet
    # Parameters - username
    # Return - None
    # Purpose - Retrieves the username the user last searched for, fetches their latest tweet from the API, then
    #           displays their username latest tweet in labels
    def latesttweet(self):
        self.cursor.execute("SELECT LastTwitterSearch FROM userInfo")
        username = self.cursor.fetchone()
        username = self.c.decrypt(username[0])
        self.lblRecentTweet.text = self.t.userLatest(username)
        self.lblRecentUsername.text = "Latest tweet from @" + username

    # Method - getmoretweets
    # Parameters - un:string
    # Return - None
    # Purpose - Obtains and displays the data on the moretweets screen using the user's chosen location
    def getmoretweets(self):
        un = self.inputTwitterUsername.text
        if un == "":
            pass
        else:
            moretwitter = self.manager.get_screen("moretwitter")
            moretwitter.layoutMoreTwitter.clear_widgets(moretwitter.layoutMoreTwitter.children)

            tweets = self.t.user10(un)
            lblun = Label(text=("Latest tweets from @" + un), size_hint_y=None)
            moretwitter.layoutMoreTwitter.add_widget(lblun)

            for i in range(9):
                lbltweet = Label(text=tweets[i], size_hint_y=None)
                lbltweet.texture_update()
                moretwitter.layoutMoreTwitter.add_widget(lbltweet)

            btnback = Button(text="Back", height=dp(40), size_hint_y=None, on_press=lambda a: self.back())
            moretwitter.layoutMoreTwitter.add_widget(btnback)
            self.manager.current = "moretwitter"

    # Method - back
    # Parameters - username: string, secureusername:s tring
    # Return - None
    # Purpose - Updates the main twitter screen with the latest tweet from the username the user last searched for,
    #           then displays the twitter screen.
    def back(self):
        username = self.inputTwitterUsername.text
        secureusername = self.c.encrypt(username)
        sql = """UPDATE userInfo SET LastTwitterSearch='{}'""".format(secureusername)
        self.cursor.execute(sql)
        self.db.commit()
        print("Last user search updated")
        self.lblRecentUsername.text = "Latest tweet from @{}".format(username)
        self.lblRecentTweet.text = self.t.userLatest(username)
        self.manager.current = "twitter"


class MoreTwitterScreen(Screen):
    def __init__(self, **kwargs):
        super(MoreTwitterScreen, self).__init__(**kwargs)

########################################################################################################################


class NotesScreen(Screen):
    # Method - NoteScreen init
    # Parameters - None
    # Return - None
    # Purpose -
    def __init__(self, **kwargs):
        super(NotesScreen, self).__init__(**kwargs)
        self.c = Crypto(False, 0)
        self.latestnote()
        self.db = sqlite3.connect("UserData.db")
        self.cursor = self.db.cursor()
        self.n = Notes()

    def latestnote(self):
        data = self.n.mostrecent()
        if data is False:
            self.lblLastNoteTitle.text = "No notes found!"
            self.lblLastNoteContent.text = " "
        else:
            recenttitle = data[0]
            recentcontent = data[1]
            recenttitle = self.c.decrypt(recenttitle)
            recentcontent = self.c.decrypt(recentcontent)
            self.lblLastNoteTitle.text = recenttitle
            self.lblLastNoteContent.text = recentcontent

    def newnote(self):
        newnotes = self.manager.get_screen("newnotes")
        newnotes.inputNewNoteTitle.text = ""
        newnotes.inputNewNoteContent.text = ""
        self.parent.current = "newnotes"

    def notesbytime(self):
        data = self.n.sort("Title")
        count = len(data)
        self.setupmorenotes(count, data)

    def notesbytitle(self):
        data = self.n.sort("Title")
        count = len(data)
        self.setupmorenotes(count, data)

    def searchnotes(self):
        searchterm = self.inputSearchNotes.text
        if searchterm == "":
            pass
        else:
            searchterm = self.c.encrypt(searchterm)
            data = self.n.search(searchterm)
            count = len(data)
            self.setupmorenotes(count, data)

    def back(self):
        self.latestnote()
        self.manager.current = "notes"

    def delete(self, noteid):
        self.n.delete(noteid)
        self.latestnote()
        self.manager.current = "notes"
        print("Note deleted")

    def edit(self, noteid):
        editnotes = self.manager.get_screen("editnotes")
        editnotes.currentnoteid = noteid
        self.manager.current = "editnotes"

    def setupmorenotes(self, count, data):
        morenotes = self.manager.get_screen("morenotes")
        morenotes.layoutMoreNotes.clear_widgets(morenotes.layoutMoreNotes.children)
        for i in range(count):
            noteid = data[i][0]
            title = data[i][1]
            title = self.c.decrypt(title)
            content = data[i][2]
            content = self.c.decrypt(content)

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

        grid = GridLayout(cols=2, size_hint_y=None)
        btnback = (Button(text="Back", height=dp(80), on_press=lambda a: self.back()))
        grid.add_widget(btnback)
        morenotes.layoutMoreNotes.add_widget(grid)
        self.manager.current = "morenotes"


class NewNotesScreen(Screen):
    def __init__(self, **kwargs):
        super(NewNotesScreen, self).__init__(**kwargs)

    def createnote(self):
        title = self.inputNewNoteTitle.text
        content = self.inputNewNoteContent.text

        if title == "" or content == "":
            pass
        else:
            c = Crypto(False, 0)
            title = c.encrypt(title)
            content = c.encrypt(content)
            n = Notes()
            n.create(title, content)
            self.manager.current = "notes"


class MoreNotesScreen(Screen):
    pass


class EditNotesScreen(Screen):
    def editnote(self):
        noteid = self.currentnoteid
        title = self.inputEditNoteTitle.text
        content = self.inputEditNoteContent.text

        c = Crypto(False, 0)
        title = c.encrypt(title)
        content = c.encrypt(content)
        n = Notes()
        n.edit(noteid, title, content)
        notes = self.manager.get_screen("notes")
        notes.latestnote()

########################################################################################################################


class RemindersScreen(Screen):
    def __init__(self, **kwargs):
        super(RemindersScreen, self).__init__(**kwargs)
        self.c = Crypto(False, 0)
        self.latestreminder()
        self.db = sqlite3.connect("UserData.db")
        self.cursor = self.db.cursor()
        self.n = Reminders()

    def latestreminder(self):
        data = self.r.mostrecent()
        if data is False:
            self.lblLastReminderTitle.text = "No reminders found!"
            self.lblLastReminderContent.text = " "
        else:
            recenttitle = data[0]
            recentcontent = data[1]
            recenttitle = self.c.decrypt(recenttitle)
            recentcontent = self.c.decrypt(recentcontent)
            self.lblLastReminderTitle.text = recenttitle
            self.lblLastReminderContent.text = recentcontent

    def newreminder(self):
        newreminders = self.manager.get_screen("newreminders")
        newreminders.inputNewReminderTitle.text = ""
        newreminders.inputNewReminderContent.text = ""
        newreminders.inputNewReminderYear.text = ""
        newreminders.inputNewReminderMonth.text = ""
        newreminders.inputNewReminderDay.text = ""
        newreminders.inputNewReminderHour.text = ""
        newreminders.inputNewReminderMinute.text = ""
        newreminders.inputNewReminderSecond.text = ""
        self.parent.current = "newreminders"

    def remindersbytime(self):
        data = self.r.sort("Time")
        count = len(data)
        self.setupmorereminders(count, data)

    def remindersbytitle(self):
        data = self.r.sort("Title")
        count = len(data)
        self.setupmorereminders(count, data)

    def searchreminders(self):
        searchterm = self.inputSearchReminders.text
        if searchterm == "":
            pass
        else:
            searchterm = self.c.encrypt(searchterm)
            data = self.r.search(searchterm)
            count = len(data)
            self.setupmorereminders(count, data)

    def setupmorereminders(self, count, data):
        morereminders = self.manager.get_screen("morereminders")
        morereminders.layoutMoreReminders.clear_widgets(morereminders.layoutMoreReminders.children)

        for i in range(count):
            reminderid = data[i][0]
            title = data[i][1]
            title = self.c.decrypt(title)
            content = data[i][2]
            content = self.c.decrypt(content)
            date = data[i][3]
            date = datetime.datetime.fromtimestamp(date)

            lbltitle = Label(text=title, size_hint_y=None)
            lbltitle.texture_update()
            morereminders.layoutMoreReminders.add_widget(lbltitle)

            lbltext = Label(text=content, size_hint_y=None)
            lbltext.texture_update()
            morereminders.layoutMoreReminders.add_widget(lbltext)

            lbldate = Label(text=str(date), size_hint_y=None)
            lbldate.texture_update()
            morereminders.layoutMoreReminders.add_widget(lbldate)

            grid = GridLayout(cols=2, size_hint_y=None)
            btnedit = Button(text="Edit", size_hint_y=None, on_press=lambda a: self.edit(reminderid))
            btndelete = Button(text="Delete", size_hint_y=None, on_press=lambda a: self.delete(reminderid))
            btnedit.texture_update()
            btndelete.texture_update()
            grid.add_widget(btnedit)
            grid.add_widget(btndelete)
            morereminders.layoutMoreReminders.add_widget(grid)

        grid = GridLayout(cols=2, size_hint_y=None)
        btnback = (Button(text="Back", height=dp(80), on_press=lambda a: self.back()))
        grid.add_widget(btnback)
        morereminders.layoutMoreReminders.add_widget(grid)
        self.manager.current = "morereminders"

    def back(self):
        self.latestreminder()
        self.manager.current = "reminders"

    def delete(self, reminderid):
        self.r.delete(reminderid)
        self.latestreminder()
        self.manager.current = "reminders"
        print("Reminder deleted")

    def edit(self, reminderid):
        editreminders = self.manager.get_screen("editreminders")
        editreminders.currentreminderid = reminderid
        self.manager.current = "editreminders"


class NewRemindersScreen(Screen):
    def __init__(self, **kwargs):
        super(NewRemindersScreen, self).__init__(**kwargs)

    def createreminder(self):
        title = self.inputNewReminderTitle.text
        content = self.inputNewReminderContent.text
        year = self.inputNewReminderYear.text
        month = self.inputNewReminderMonth.text
        day = self.inputNewReminderDay.text
        hour = self.inputNewReminderHour.text
        minute = self.inputNewReminderMinute.text
        second = self.inputNewReminderSecond.text

        if title == "" or content == "" or year == "" or month == "" or day == "" or hour == "" or minute == "" or second == "":
            print("Missing values")
        else:
            if year.isnumeric is False or month.isnumeric is False or day.isnumeric is False or hour.isnumeric is False or minute.isnumeric is False or second.isnumeric is False:
                print("Non-numeric values")
            else:
                c = Crypto(False, 0)
                title = c.encrypt(title)
                content = c.encrypt(content)
                r = Reminders()
                r.create(title, content, int(year), int(month), int(day), int(hour), int(minute), int(second))
                self.manager.current = "reminders"


class MoreRemindersScreen(Screen):
    pass


class EditRemindersScreen(Screen):
    def editreminder(self):
        reminderid = self.currentreminderid
        title = self.inputEditReminderTitle.text
        content = self.inputEditReminderContent.text
        c = Crypto(False, 0)
        title = c.encrypt(title)
        content = c.encrypt(content)
        n = Reminders()
        n.edit(reminderid, title, content)
        reminders = self.manager.get_screen("reminders")
        reminders.latestreminder()

########################################################################################################################


class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)

    def changename(self):
        name = self.inputNewName.text
        if name == "":
            pass
        else:
            s = Settings()
            s.changeName(name)
            print("Name changed successfully")

    def changelocation(self):
        city = self.inputNewCity.text
        country = self.inputNewCountry.text
        if city == "" or country == "":
            pass
        else:
            s = Settings()
            s.changeLocation(country, city)
            print("Location changed successfully")

    def restartsetup(self):
        pass


class SetupScreen(Screen):
    def __init__(self, **kwargs):
        super(SetupScreen, self).__init__(**kwargs)

    def completesetup(self):
        name = self.inputName.text
        city = self.inputCity.text
        country = self.inputCountry.text

        if name == "" or city == "" or country == "":
            pass
        else:
            setup = Setup()
            setup.completeSetup(name, country, city)
            print("Setup complete")
            sm.add_widget(HomeScreen(name="home"))
            sm.add_widget(WeatherScreen(name="weather"))
            sm.add_widget(TwitterScreen(name="twitter"))
            sm.add_widget(NotesScreen(name="notes"))
            sm.add_widget(RemindersScreen(name="reminders"))
            sm.add_widget(ExportScreen(name="export"))
            self.parent.current = "home"


class ExportScreen(Screen):
    def __init__(self, **kwargs):
        super(ExportScreen, self).__init__(**kwargs)
        self.c = csvworker()

    def exportnotes(self):
        self.c.exportcsv("Note")
        self.parent.current = "email"

    def exportreminders(self):
        self.c.exportcsv("Reminder")
        self.parent.current = "email"


class EmailScreen(Screen):
    def __init__(self, **kwargs):
        super(EmailScreen, self).__init__(**kwargs)
        # work in toggle buttons for different services???

    def sendemail(self):
        c = csvworker()
        username = self.inputEmailUsername.text
        password = self.inputEmailPassword.text
        target = self.inputEmailTarget.text
        c.email(username, password, target)

########################################################################################################################


sm = ScreenManager()


class AssistantApp(App):
    title = 'Assistant'

    def addscreens(self):
        sm.add_widget(MoreWeatherScreen(name="moreweather"))
        sm.add_widget(MoreTwitterScreen(name="moretwitter"))
        sm.add_widget(NewNotesScreen(name="newnotes"))
        sm.add_widget(MoreNotesScreen(name="morenotes"))
        sm.add_widget(EditNotesScreen(name="editnotes"))
        sm.add_widget(NewRemindersScreen(name="newreminders"))
        sm.add_widget(MoreRemindersScreen(name="morereminders"))
        sm.add_widget(EditRemindersScreen(name="editreminders"))
        sm.add_widget(SettingsScreen(name="settings"))
        sm.add_widget(EmailScreen(name="email"))

    def build(self):
        self.icon = "icon.png"
        return sm
        
    def on_start(self):
        if os.path.exists("UserData.db") is True:
            print("Userdata.db found")
            sm.add_widget(HomeScreen(name="home"))
            sm.add_widget(WeatherScreen(name="weather"))
            sm.add_widget(TwitterScreen(name="twitter"))
            sm.add_widget(NotesScreen(name="notes"))
            sm.add_widget(RemindersScreen(name="reminders"))
            sm.add_widget(ExportScreen(name="export"))
            self.addscreens()
            self.root.current = "home"
        else:
            print("Userdata.db not found")
            sm.add_widget(SetupScreen(name="setup"))
            self.addscreens()
            self.root.current = "setup"


if __name__ == "__main__":
    app = AssistantApp()
    Window.size = (360, 640)
    app.run()
