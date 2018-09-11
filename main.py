# -*- coding: utf-8 -*-

import sqlite3
import os.path

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen

from weather import Weather4Day, Weather10Day
from settings import Setup
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
            self.lblName = "Welcome, {}!".format(username[0])

########################################################################################################################


class WeatherScreen(Screen):
    def __init__(self, **kwargs):
        super(WeatherScreen, self).__init__(**kwargs)
        self.getweather()

    def getweather(self):
        with sqlite3.connect("UserData.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT city FROM userInfo")
            city = cursor.fetchone()
            cursor.execute("SELECT country FROM userInfo")
            country = cursor.fetchone()
        city = city[0]
        country = country[0]

        w = Weather4Day(country, city)

        self.latestLocation = "The weather in {}, {} is".format(city, country)
        self.latestWeatherText = w.forecastTodayText()
        self.latestWeatherHigh = w.forecastTodayHigh() + "C"
        self.latestWeatherLow = w.forecastTodayLow() + "C"

    def getmoreweather(self):
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

########################################################################################################################


class TwitterScreen(Screen):

    def __init__(self, **kwargs):
        super(TwitterScreen, self).__init__(**kwargs)
        self.latesttweet()

    def latesttweet(self):
        with sqlite3.connect("UserData.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT LastTwitterSearch FROM userInfo")
            username = cursor.fetchone()

        username = username[0]
        t = Twitter()
        self.recentTweet = t.userLatest(username)
        self.recentUsername = "Latest tweet from @" + username

    def getmoretweets(self):
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
            self.manager.current = "moretwitter"

    def back(self):
        username = self.inputTwitterUsername.text

        t = Twitter()
        t.updateUser(username)
        self.recentUsername = "Latest tweet from @{}".format(username)
        self.recentTweet = t.userLatest(username)
        self.manager.current = "twitter"


class MoreTwitterScreen(Screen):
    def __init__(self, **kwargs):
        super(MoreTwitterScreen, self).__init__(**kwargs)

########################################################################################################################


class NotesScreen(Screen):
    def __init__(self, **kwargs):
        super(NotesScreen, self).__init__(**kwargs)

    def newnote(self):
        self.parent.current = "newnotes"

    def notesbytime(self):
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
            # FIX THIS
            btnedit = Button(text="Edit", size_hint_y=None, on_press=lambda a: self.edit(noteid))
            btndelete = Button(text="Delete", size_hint_y=None, on_press=lambda a: self.delete(noteid))
            btnedit.texture_update()
            btndelete.texture_update()
            grid.add_widget(btnedit)
            grid.add_widget(btndelete)
            morenotes.layoutMoreNotes.add_widget(grid)

        morenotes.layoutMoreNotes.add_widget(Button(text="Back", height=dp(80), on_press=lambda a: self.back()))
        self.manager.current = "morenotes"

    def notesbytitle(self):
        morenotes = self.manager.get_screen("morenotes")
        morenotes.layoutMoreNotes.clear_widgets(morenotes.layoutMoreNotes.children)

        with sqlite3.connect("UserData.db") as db:
            cursor = db.cursor()
            sql = """SELECT NoteID, Title, Content FROM Notes ORDER BY Title"""
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
            # FIX THIS
            btnedit = Button(text="Edit", size_hint_y=None, on_press=lambda a: self.edit(noteid))
            btndelete = Button(text="Delete", size_hint_y=None, on_press=lambda a: self.delete(noteid))
            btnedit.texture_update()
            btndelete.texture_update()
            grid.add_widget(btnedit)
            grid.add_widget(btndelete)
            morenotes.layoutMoreNotes.add_widget(grid)

        morenotes.layoutMoreNotes.add_widget(Button(text="Back", height=dp(80), on_press=lambda a: self.back()))
        self.manager.current = "morenotes"

    def back(self):
        self.manager.current = "notes"

    def delete(self, noteid):
        n = Notes()
        n.delete(noteid)
        self.manager.current = "notes"
        print("Note deleted")

    def edit(self, noteid):
        print(noteid)
        editnotes = self.manager.get_screen("editnotes")
        editnotes.currentnoteid = noteid
        self.manager.current = "editnotes"


class NewNotesScreen(Screen):
    def __init__(self, **kwargs):
        super(NewNotesScreen, self).__init__(**kwargs)

    def createnote(self):
        title = self.inputNewNoteTitle.text
        content = self.inputNewNoteContent.text

        if title == "" or content == "":
            pass
        else:
            n = Notes()
            n.create(title, content)
            self.parent.current = "notes"


class MoreNotesScreen(Screen):
    pass


class EditNotesScreen(Screen):
    def editnote(self):
        print(self.currentnoteid)
        noteid = self.currentnoteid
        print(noteid)
        notes = self.manager.get_screen("notes")
        title = self.inputEditNoteTitle.text
        content = self.inputEditNoteContent.text

        n = Notes()
        n.edit(noteid, title, content)

########################################################################################################################


class RemindersScreen(Screen):
    def __init__(self, **kwargs):
        super(RemindersScreen, self).__init__(**kwargs)

    def newreminder(self):
        self.parent.current = "newreminders"

    def remindersbytime(self):
        morereminders = self.manager.get_screen("morereminders")
        morereminders.layoutMoreReminders.clear_widgets(morereminders.layoutMoreReminders.children)

        with sqlite3.connect("UserData.db") as db:
            cursor = db.cursor()
            sql = """SELECT ReminderID, Title, Content FROM Reminders ORDER BY Date"""
            cursor.execute(sql)
            data = cursor.fetchall()
            sql = """SELECT Count(ReminderID) FROM Reminders"""
            cursor.execute(sql)
            count = cursor.fetchall()
            count = count[0][0]

        for i in range(count):
            reminderid = data[i][0]
            title = data[i][1]
            content = data[i][2]

            lbltitle = Label(text=title, size_hint_y=None)
            lbltitle.texture_update()
            morereminders.layoutMoreReminders.add_widget(lbltitle)

            lbltext = Label(text=content, size_hint_y=None)
            lbltext.texture_update()
            morereminders.layoutMoreReminders.add_widget(lbltext)

            grid = GridLayout(cols=2, size_hint_y=None)
            # FIX THIS
            btnedit = Button(text="Edit", size_hint_y=None, on_press=lambda a: self.edit(reminderid))
            btndelete = Button(text="Delete", size_hint_y=None, on_press=lambda a: self.delete(reminderid))
            btnedit.texture_update()
            btndelete.texture_update()
            grid.add_widget(btnedit)
            grid.add_widget(btndelete)
            morereminders.layoutMoreReminders.add_widget(grid)

        morereminders.layoutMoreReminders.add_widget(Button(text="Back", height=dp(80), on_press=lambda a: self.back()))
        self.manager.current = "morereminders"

    def remindersbytitle(self):
        morereminders = self.manager.get_screen("morereminders")
        morereminders.layoutMoreReminders.clear_widgets(morereminders.layoutMoreReminders.children)

        with sqlite3.connect("UserData.db") as db:
            cursor = db.cursor()
            sql = """SELECT ReminderID, Title, Content FROM Reminders ORDER BY Title"""
            cursor.execute(sql)
            data = cursor.fetchall()
            sql = """SELECT Count(ReminderID) FROM Reminders"""
            cursor.execute(sql)
            count = cursor.fetchall()
            count = count[0][0]

        for i in range(count):
            reminderid = data[i][0]
            title = data[i][1]
            content = data[i][2]

            lbltitle = Label(text=title, size_hint_y=None)
            lbltitle.texture_update()
            morereminders.layoutMoreReminders.add_widget(lbltitle)

            lbltext = Label(text=content, size_hint_y=None)
            lbltext.texture_update()
            morereminders.layoutMoreReminders.add_widget(lbltext)

            grid = GridLayout(cols=2, size_hint_y=None)
            # FIX THIS
            btnedit = Button(text="Edit", size_hint_y=None, on_press=lambda a: self.edit(reminderid))
            btndelete = Button(text="Delete", size_hint_y=None, on_press=lambda a: self.delete(reminderid))
            btnedit.texture_update()
            btndelete.texture_update()
            grid.add_widget(btnedit)
            grid.add_widget(btndelete)
            morereminders.layoutMoreReminders.add_widget(grid)

        morereminders.layoutMoreReminders.add_widget(Button(text="Back", height=dp(80), on_press=lambda a: self.back()))
        self.manager.current = "morereminders"

    def back(self):
        self.manager.current = "reminders"

    def delete(self, reminderid):
        n = Reminders()
        n.delete(reminderid)
        self.manager.current = "reminders"
        print("Reminder deleted")

    def edit(self, reminderid):
        print(reminderid)
        editreminders = self.manager.get_screen("editreminders")
        editreminders.currentreminderid = reminderid
        self.manager.current = "editreminders"


class NewRemindersScreen(Screen):
    def __init__(self, **kwargs):
        super(NewRemindersScreen, self).__init__(**kwargs)

    def createreminder(self):
        title = self.inputNewReminderTitle.text
        content = self.inputNewReminderContent.text

        if title == "" or content == "":
            pass
        else:
            n = Reminders()
            n.create(title, content)
            self.parent.current = "reminders"


class MoreRemindersScreen(Screen):
    pass


class EditRemindersScreen(Screen):
    def editreminder(self):
        print(self.currentreminderid)
        reminderid = self.currentreminderid
        print(reminderid)
        reminders = self.manager.get_screen("reminders")
        title = self.inputEditReminderTitle.text
        content = self.inputEditReminderContent.text

        n = Reminders()
        n.edit(reminderid, title, content)

########################################################################################################################


class AlarmsScreen(Screen):
    pass


class NewAlarmsScreen(Screen):
    pass


class MoreAlarmsScreen(Screen):
    pass


class EditAlarmsScreen(Screen):
    pass

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

    def changelocation(self):
        city = self.inputNewCity.text
        country = self.inputNewCountry.text
        if city == "" or country == "":
            pass
        else:
            s = Settings()
            s.changeLocation(country, city)

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
            setup.completesetup(name, country, city)
            self.parent.current = "home"

########################################################################################################################


class MyScreenManager(ScreenManager):
    pass


class AssistantApp(App):
    title = 'Assistant'
        
    def on_start(self):
        if os.path.exists("UserData.db") is True:
            print("Userdata.db found")
            self.root.current = "home"
        else:
            print("Userdata.db not found")
            self.manager.current = "setup"


if __name__ == "__main__":
    app = AssistantApp()
    Window.size = (360, 640)
    app.run()
