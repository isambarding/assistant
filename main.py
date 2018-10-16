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

            for i in range(len(days)):
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
        self.lblRecentTweet.text = self.t.userlatest(username)
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

            for i in range(len(tweets)):
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
        self.lblRecentUsername.text = "Latest tweet from @{}".format(username)
        self.lblRecentTweet.text = self.t.userlatest(username)
        self.manager.current = "twitter"


class MoreTwitterScreen(Screen):
    def __init__(self, **kwargs):
        super(MoreTwitterScreen, self).__init__(**kwargs)

########################################################################################################################


class NotesScreen(Screen):
    # Method - NoteScreen init
    # Parameters - None
    # Return - None
    # Purpose -  Initialises instances of the notes and crypto classes, connects to the database, and runs the
    #            latestnote method
    def __init__(self, **kwargs):
        super(NotesScreen, self).__init__(**kwargs)
        self.c = Crypto(False, 0)
        self.n = Notes()
        self.latestnote()
        self.db = sqlite3.connect("UserData.db")
        self.cursor = self.db.cursor()

    # Method - latestnote
    # Parameters - data: list of strings
    # Return - None
    # Purpose - If the user has any notes, display the most recent one in labels
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

    # Method - newnote
    # Parameters - None
    # Return - None
    # Purpose - Clears the content of the text inputs of the newnotes screen, then displays it
    def newnote(self):
        newnotes = self.manager.get_screen("newnotes")
        newnotes.inputNewNoteTitle.text = ""
        newnotes.inputNewNoteContent.text = ""
        self.parent.current = "newnotes"

    # Method - notesbytime
    # Parameters - data: list of strings
    # Return - None
    # Purpose - Retrieves a list of the user's notes sorted by time, then passes it to the setupmorenotes function
    def notesbytime(self):
        data = self.n.sort("Title")
        count = len(data)
        self.setupmorenotes(count, data)

    # Method - notesbytime
    # Parameters - data: list of strings
    # Return - None
    # Purpose - Retrieves a list of the user's notes sorted by title alphabetically, then passes it to the
    #           setupmorenotes function
    def notesbytitle(self):
        data = self.n.sort("Title")
        count = len(data)
        self.setupmorenotes(count, data)

    # Method - searchnotes
    # Parameters - searchterm: string, data: list of strings
    # Return - None
    # Purpose - Gets a list of the user's notes containing a given search term, then passes it to the setupmorenotes
    #           function
    def searchnotes(self):
        searchterm = self.inputSearchNotes.text
        if searchterm == "":
            pass
        else:
            searchterm = self.c.encrypt(searchterm)
            data = self.n.search(searchterm)
            count = len(data)
            self.setupmorenotes(count, data)

    # Method - back
    # Parameters - None
    # Return - None
    # Purpose - Runs the latestnote method, then displays the notes screen
    def back(self):
        self.latestnote()
        self.manager.current = "notes"

    # Method - delete
    # Parameters - noteid: string
    # Return - None
    # Purpose - Deletes the note corresponding to the given noteid, then calls the latestnote method and displays the
    #           notes screen
    def delete(self, noteid):
        self.n.delete(noteid)
        self.latestnote()
        self.manager.current = "notes"

    # Method - edit
    # Parameters - noteid: string
    # Return - None
    # Purpose - Displays the editnotes screen, and passes noteid to it
    def edit(self, noteid):
        editnotes = self.manager.get_screen("editnotes")
        editnotes.currentnoteid = noteid
        self.manager.current = "editnotes"

    # Method - setupmorenotes
    # Parameters - count: integer , data: list of strings
    # Return - None
    # Purpose - Adds widgets displaying the title and content of each note within the given list, as well as their
    # corresponding edit and delete buttons to the morenotes screen. A "back" button is then added and the screen is
    # displayed.
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

    # Method - createnote
    # Parameters - title: string, content: string
    # Return - None
    # Purpose - Encrypts the title and content and passes them to the create method, then displays the notes screen
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
            notes = self.manager.get_screen("notes")
            notes.latestnote()
            self.manager.current = "notes"


class MoreNotesScreen(Screen):
    pass


class EditNotesScreen(Screen):
    # Method - editnote
    # Parameters - noteid: string, title: string, content: string
    # Return - None
    # Purpose - Encrypts the title and content and passes them to the edit method, then displays the notes screen
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
        self.manager.current = "notes"

########################################################################################################################


class RemindersScreen(Screen):
    # Method - RemindersScreen init
    # Parameters - None
    # Return - None
    # Purpose -  Initialises instances of the reminders and crypto classes, connects to the database, and runs the
    #            latestreminder method
    def __init__(self, **kwargs):
        super(RemindersScreen, self).__init__(**kwargs)
        self.c = Crypto(False, 0)
        self.r = Reminders()
        self.latestreminder()
        self.db = sqlite3.connect("UserData.db")
        self.cursor = self.db.cursor()

    # Method - latestreminder
    # Parameters - data: list of strings
    # Return - None
    # Purpose - If the user has any reminders, display the most recent one in labels
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

    # Method - newreminder
    # Parameters - None
    # Return - None
    # Purpose - Clears the content of the text inputs of the newreminder screen, then displays it
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

    # Method - remindersbytime
    # Parameters - data: list of strings
    # Return - None
    # Purpose - Retrieves a list of the user's reminders sorted by time, then passes it to the setupmorereminders 
    # function
    def remindersbytime(self):
        data = self.r.sort("Time")
        count = len(data)
        self.setupmorereminders(count, data)

    # Method - remindersbytime
    # Parameters - data: list of strings
    # Return - None
    # Purpose - Retrieves a list of the user's reminders sorted by title alphabetically, then passes it to the
    #           setupmorereminders function
    def remindersbytitle(self):
        data = self.r.sort("Title")
        count = len(data)
        self.setupmorereminders(count, data)

    # Method - searchreminders
    # Parameters - searchterm: string, data: list of strings
    # Return - None
    # Purpose - Gets a list of the user's reminders containing a given search term, then passes it to the 
    # setupmorereminders function
    def searchreminders(self):
        searchterm = self.inputSearchReminders.text
        if searchterm == "":
            pass
        else:
            searchterm = self.c.encrypt(searchterm)
            data = self.r.search(searchterm)
            count = len(data)
            self.setupmorereminders(count, data)

    # Method - setupmorereminders
    # Parameters - count: integer , data: list of strings
    # Return - None
    # Purpose - Adds widgets displaying the title and content of each reminder within the given list, as well as their
    # corresponding edit and delete buttons to the morereminders screen. A "back" button is then added and the screen is
    # displayed.
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

    # Method - back
    # Parameters - None
    # Return - None
    # Purpose - Runs the latestreminder method, then displays the reminders screen
    def back(self):
        self.latestreminder()
        self.manager.current = "reminders"

    # Method - delete
    # Parameters - reminderid: string
    # Return - None
    # Purpose - Deletes the reminder corresponding to the given reminderid, then calls the latestreminder method and 
    # displays the reminders screen
    def delete(self, reminderid):
        self.r.delete(reminderid)
        self.latestreminder()
        self.manager.current = "reminders"

    # Method - edit
    # Parameters - reminderid: string
    # Return - None
    # Purpose - Displays the editreminders screen, and passes reminderid to it
    def edit(self, reminderid):
        editreminders = self.manager.get_screen("editreminders")
        editreminders.currentreminderid = reminderid
        self.manager.current = "editreminders"


class NewRemindersScreen(Screen):
    def __init__(self, **kwargs):
        super(NewRemindersScreen, self).__init__(**kwargs)

    # Method - createreminder
    # Parameters - title: string, content: string
    # Return - None
    # Purpose - Encrypts the title and content and passes them and the given times to the create method, then displays 
    # the reminders screen
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
            pass
        else:
            if year.isnumeric is False or month.isnumeric is False or day.isnumeric is False or hour.isnumeric is False or minute.isnumeric is False or second.isnumeric is False:
                pass
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
    # Method - editreminder
    # Parameters - reminderid: string, title: string, content: string
    # Return - None
    # Purpose - Encrypts the title and content and passes them to the edit method, then displays the reminders screen
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

    # Method - changename
    # Parameters - name: string
    # Return - None
    # Purpose - Passes the user's given name to the changename method in settings.py, if a name has been given
    def changename(self):
        name = self.inputNewName.text
        if name == "":
            pass
        else:
            s = Settings()
            s.changename(name)

    # Method - changelocation
    # Parameters - city: string, country: string
    # Return - None
    # Purpose - If a city or country has been given, pass them to the changelocation method in settings.py
    def changelocation(self):
        city = self.inputNewCity.text
        country = self.inputNewCountry.text
        if city == "" or country == "":
            pass
        else:
            s = Settings()
            s.changelocation(country, city)


class SetupScreen(Screen):
    def __init__(self, **kwargs):
        super(SetupScreen, self).__init__(**kwargs)

    # Method - completesetup
    # Parameters - name: string, city: string, country: string
    # Return - None
    # Purpose - If a name, city, and country have been given, pass them to the completesetup method in settings.py, then
    #           add the screens that require completesetup to have run, then show the home screen
    def completesetup(self):
        name = self.inputName.text
        city = self.inputCity.text
        country = self.inputCountry.text

        if name == "" or city == "" or country == "":
            pass
        else:
            setup = Setup()
            setup.completesetup(name, country, city)
            sm.add_widget(HomeScreen(name="home"))
            sm.add_widget(WeatherScreen(name="weather"))
            sm.add_widget(TwitterScreen(name="twitter"))
            sm.add_widget(NotesScreen(name="notes"))
            sm.add_widget(RemindersScreen(name="reminders"))
            sm.add_widget(ExportScreen(name="export"))
            self.parent.current = "home"


class ExportScreen(Screen):
    # Method - ExportScreen init
    # Parameters - None
    # Return - None
    # Purpose - Initialises an instance of csvworker for this screen
    def __init__(self, **kwargs):
        super(ExportScreen, self).__init__(**kwargs)
        self.c = csvworker()

    # Method - exportnotes
    # Parameters - None
    # Return - None
    # Purpose - Pass "Note" to the exportcsv method, then display the email screen
    def exportnotes(self):
        self.c.exportcsv("Note")
        self.parent.current = "email"

    # Method - exportreminders
    # Parameters - None
    # Return - None
    # Purpose - Pass "Reminder" to the exportcsv method, then display the email screen
    def exportreminders(self):
        self.c.exportcsv("Reminder")
        self.parent.current = "email"


class EmailScreen(Screen):
    def __init__(self, **kwargs):
        super(EmailScreen, self).__init__(**kwargs)

    # Method - sendemail
    # Parameters - username: string, password: string, target: string
    # Return - None
    # Purpose - Initialises csvworker, fetches the user's username, password, and target email, then passes them to the
    #           email method
    def sendemail(self):
        c = csvworker()
        username = self.inputEmailUsername.text
        password = self.inputEmailPassword.text
        target = self.inputEmailTarget.text
        if c.email(username, password, target) == False:
            self.parent.current = "home"

########################################################################################################################

# Initialise a screenmanager
sm = ScreenManager()


class AssistantApp(App):
    # Sets the app title to "Assistant"
    title = "Assistant"

    # Method - addscreens
    # Parameters - None
    # Return - None
    # Purpose - Adds screens that do not require setup to be completed
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

    # Method - build
    # Parameters - None
    # Return - sm (screen manager)
    # Purpose - Kivy method. Adds the screen manager which contains all the screens to be displayed. Also used to
    #           set the app icon.
    def build(self):
        self.icon = "icon.png"
        return sm

    # Method - on_start
    # Parameters - None
    # Return - None
    # Purpose - Kivy method. Checks if the database exists- if yes, all screens are added and the home screen is
    #           displayed. If no, the setup screen and the screens in addscreens are added, then the setup screen is
    #           displayed.
    def on_start(self):
        if os.path.exists("UserData.db") is True:
            sm.add_widget(HomeScreen(name="home"))
            sm.add_widget(WeatherScreen(name="weather"))
            sm.add_widget(TwitterScreen(name="twitter"))
            sm.add_widget(NotesScreen(name="notes"))
            sm.add_widget(RemindersScreen(name="reminders"))
            sm.add_widget(ExportScreen(name="export"))
            self.addscreens()
            self.root.current = "home"
        else:
            sm.add_widget(SetupScreen(name="setup"))
            self.addscreens()
            self.root.current = "setup"

# Create the app, set the window size, then run the app.
if __name__ == "__main__":
    app = AssistantApp()
    Window.size = (360, 640)
    app.run()
