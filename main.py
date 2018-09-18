# -*- coding: utf-8 -*-

import sqlite3
import os.path

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

from weather import Weather4Day, Weather10Day
from settings import Setup, Settings
from twitter import Twitter
from encryption import Crypto
from NotesRemindersAlarms import NotesRemindersAlarms, Notes, Reminders, Alarms

from kivy.core.window import Window
from kivy.uix.label import Label 
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.metrics import dp

Builder.load_file("assistant.txt")


class HomeScreen(Screen):
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
        c = Crypto(False, 0)
        city = c.decrypt(city[0])
        country = c.decrypt(country[0])

        w = Weather4Day(country, city)

        self.lblLocation.text = "The weather in {}, {} is".format(city, country)
        self.lblWeatherText.text = w.forecastTodayText()
        self.lblWeatherHigh.text = w.forecastTodayHigh() + "C"
        self.lblWeatherLow.text = w.forecastTodayLow() + "C"

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
        self.c = Crypto(False, 0)
        self.t = Twitter()
        self.latesttweet()

    def latesttweet(self):
        with sqlite3.connect("UserData.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT LastTwitterSearch FROM userInfo")
            username = cursor.fetchone()

        username = self.c.decrypt(username[0])
        self.lblRecentTweet.text = self.t.userLatest(username)
        self.lblRecentUsername.text = "Latest tweet from @" + username

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

    def back(self):
        username = self.inputTwitterUsername.text
        secureusername = self.c.encrypt(username)

        with sqlite3.connect("UserData.db") as db:
            cursor = db.cursor()
            sql = """UPDATE userInfo SET LastTwitterSearch='{}'""".format(secureusername)
            cursor.execute(sql)
            db.commit()
        print("Last user search updated")

        self.lblRecentUsername.text = "Latest tweet from @{}".format(username)
        self.lblRecentTweet.text = self.t.userLatest(username)
        self.manager.current = "twitter"


class MoreTwitterScreen(Screen):
    def __init__(self, **kwargs):
        super(MoreTwitterScreen, self).__init__(**kwargs)

########################################################################################################################


class NotesScreen(Screen):
    def __init__(self, **kwargs):
        super(NotesScreen, self).__init__(**kwargs)
        self.c = Crypto(False, 0)
        self.latestnote()

    def latestnote(self):
        n = Notes()
        data = n.mostrecent()
        if data is False:
            self.lblLastNoteTitle.text = "No notes found!"
            self.lblLastNoteContent.text = " "
        else:
            recenttitle = data[0]
            recentcontent = data[1]
            self.lblLastNoteTitle.text = recenttitle
            self.lblLastNoteContent.text = recentcontent

    def newnote(self):
        newnotes = self.manager.get_screen("newnotes")
        newnotes.inputNewNoteTitle.text = ""
        newnotes.inputNewNoteContent.text = ""
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

    def searchnotes(self):
        searchterm = self.inputSearchNotes.text
        if searchterm == "":
            pass
        else:
            morenotes = self.manager.get_screen("morenotes")
            morenotes.layoutMoreNotes.clear_widgets(morenotes.layoutMoreNotes.children)

            with sqlite3.connect("UserData.db") as db:
                cursor = db.cursor()
                sql = """SELECT NoteID, Title, Content FROM Notes WHERE Content LIKE '%{}%'""".format(searchterm)
                cursor.execute(sql)
                data = cursor.fetchall()
                print(data)
                sql = """SELECT Count(NoteID) FROM Notes WHERE Title LIKE '&{}&'""".format(searchterm)
                cursor.execute(sql)
                count = cursor.fetchall()
                count = count[0][0]
                print(count)

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
        self.latestnote()
        self.manager.current = "notes"

    def delete(self, noteid):
        n = Notes()
        n.delete(noteid)
        self.latestnote()
        self.manager.current = "notes"
        print("Note deleted")

    def edit(self, noteid):
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

    def latestreminder(self):
        n = Reminders()
        data = n.mostrecent()
        if data is False:
            self.lblLastReminderTitle.text = "No reminders found!"
            self.lblLastReminderContent.text = " "
        else:
            recenttitle = data[0]
            recentcontent = data[1]
            self.lblLastReminderTitle.text = recenttitle
            self.lblLastReminderContent.text = recentcontent

    def newreminder(self):
        newreminders = self.manager.get_screen("newreminders")
        newreminders.inputNewReminderTitle.text = ""
        newreminders.inputNewReminderContent.text = ""
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
            title = self.c.decrypt(title)
            content = data[i][2]
            content = self.c.decrypt(content)

            lbltitle = Label(text=title, size_hint_y=None)
            lbltitle.texture_update()
            morereminders.layoutMoreReminders.add_widget(lbltitle)

            lbltext = Label(text=content, size_hint_y=None)
            lbltext.texture_update()
            morereminders.layoutMoreReminders.add_widget(lbltext)

            grid = GridLayout(cols=2, size_hint_y=None)
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
            title = self.c.decrypt(title)
            content = data[i][2]
            content = self.c.decrypt(content)

            lbltitle = Label(text=title, size_hint_y=None)
            lbltitle.texture_update()
            morereminders.layoutMoreReminders.add_widget(lbltitle)

            lbltext = Label(text=content, size_hint_y=None)
            lbltext.texture_update()
            morereminders.layoutMoreReminders.add_widget(lbltext)

            grid = GridLayout(cols=2, size_hint_y=None)
            btnedit = Button(text="Edit", size_hint_y=None, on_press=lambda a: self.edit(reminderid))
            btndelete = Button(text="Delete", size_hint_y=None, on_press=lambda a: self.delete(reminderid))
            btnedit.texture_update()
            btndelete.texture_update()
            grid.add_widget(btnedit)
            grid.add_widget(btndelete)
            morereminders.layoutMoreReminders.add_widget(grid)

        morereminders.layoutMoreReminders.add_widget(Button(text="Back", height=dp(80), on_press=lambda a: self.back()))
        self.manager.current = "morereminders"

    def searchreminders(self):
        searchterm = self.inputSearchReminders.text
        if searchterm == "":
            pass
        else:
            morereminders = self.manager.get_screen("morereminders")
            morereminders.layoutMoreReminders.clear_widgets(morereminders.layoutMoreReminders.children)

            with sqlite3.connect("UserData.db") as db:
                cursor = db.cursor()
                sql = """SELECT ReminderID, Title, Content FROM Reminders WHERE Content LIKE '%{}%'""".format(searchterm)
                cursor.execute(sql)
                data = cursor.fetchall()
                print(data)
                sql = """SELECT Count(ReminderID) FROM Reminders WHERE Title LIKE '&{}&'""".format(searchterm)
                cursor.execute(sql)
                count = cursor.fetchall()
                count = count[0][0]
                print(count)

            for i in range(count):
                reminderid = data[i][0]
                title = data[i][1]
                title = self.c.decrypt(title)
                content = data[i][2]
                content = self.c.decrypt(content)

                lbltitle = Label(text=title, size_hint_y=None)
                lbltitle.texture_update()
                morereminders.layoutMoreReminders.add_widget(lbltitle)

                lbltext = Label(text=content, size_hint_y=None)
                lbltext.texture_update()
                morereminders.layoutMoreReminders.add_widget(lbltext)

                grid = GridLayout(cols=2, size_hint_y=None)
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
        self.latestreminder()
        self.manager.current = "reminders"

    def delete(self, reminderid):
        n = Reminders()
        n.delete(reminderid)
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

        if title == "" or content == "":
            pass
        else:
            c = Crypto(False, 0)
            title = c.encrypt(title)
            content = c.encrypt(content)
            n = Reminders()
            n.create(title, content)
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
            sm.add_widget(AlarmsScreen(name="alarms"))
            self.parent.current = "home"

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
        sm.add_widget(NewAlarmsScreen(name="newalarms"))
        sm.add_widget(MoreAlarmsScreen(name="morealarms"))
        sm.add_widget(EditAlarmsScreen(name="editalarms"))
        sm.add_widget(SettingsScreen(name="settings"))

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
            sm.add_widget(AlarmsScreen(name="alarms"))
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
