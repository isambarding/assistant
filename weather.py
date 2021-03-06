import requests


class Weather4Day:
    # Method - Weather4Day init
    # Parameters - country: string, city: string
    # Return - None
    # Purpose - Makes an api call for the next 4 days of weather using the country and city arguments, then parses the
    #           data as json format.
    def __init__(self, country, city):
        try:
            url = "http://api.wunderground.com/api/034fa2c65c35e441/forecast/q/{}/{}.json".format(country, city)
            response = requests.get(url)
            self.data = response.json()
            print(self.data)
        except:
            self.data = "Can't connect"

    # Method - forecasttodaytext
    # Parameters - None
    # Return - s: string
    # Purpose - Gets the text forecast for the current day
    def forecasttodaytext(self):
        try:
            for day in self.data["forecast"]["txt_forecast"]["forecastday"]:
                if day["period"] == 0:
                    s = day["fcttext_metric"]
            return s
        except:
            return "No forecast found!"

    # Method - forecasttodayhigh
    # Parameters - None
    # Return - s: integer
    # Purpose - Gets the highest forecast temperature for the current day
    def forecasttodayhigh(self):
        try:
            for day in self.data["forecast"]["simpleforecast"]["forecastday"]:
                if day["period"] == 1:
                    s = day["high"]["celsius"]
            return s
        except:
            return ""

    # Method - forecasttodaylow
    # Parameters - None
    # Return - s: integer
    # Purpose - Gets the highest forecast temperature for the current day
    def forecasttodaylow(self):
        try:
            for day in self.data["forecast"]["simpleforecast"]["forecastday"]:
                if day["period"] == 1:
                   s = day["low"]["celsius"]
            return s
        except:
            return ""


class Weather10Day:
    # Method - Weather10Day init
    # Parameters - country: string, city: string
    # Return - None
    # Purpose - Makes an api call for the next 10 days of weather using the country and city arguments, then parses the
    #           data as json format.
    def __init__(self, country, city):
        try:
            url = "http://api.wunderground.com/api/034fa2c65c35e441/forecast10day/q/{}/{}.json".format(country, city)
            response = requests.get(url)
            self.data = response.json()
        except:
            self.data = "Can't connect"

    # Method - forecast10daystext
    # Parameters - None
    # Return - s: list of strings
    # Purpose - Gets the next 10 days of text forecasts
    def forecast10daystext(self):
        s = []
        try:
            for day in self.data["forecast"]["txt_forecast"]["forecastday"]:
                # Only days, not nights
                if day["period"] % 2 == 0:
                    s.append(day["fcttext_metric"])
            return s
        except:
            return ["No forecast found!"]

    # Method - forecast10dayshigh
    # Parameters - None
    # Return - s: list of strings
    # Purpose - Gets the next 10 days of highest forecast temperatures
    def forecast10dayshigh(self):
        s = []
        try:
            for day in self.data["forecast"]["simpleforecast"]["forecastday"]:
                s.append(day["high"]["celsius"])
            return s
        except:
            return [""]

    # Method - forecast10dayslow
    # Parameters - None
    # Return - s: list of strings
    # Purpose - Gets the next 10 days of lowest forecast temperatures
    def forecast10dayslow(self):
        s = []
        try:
            for day in self.data["forecast"]["simpleforecast"]["forecastday"]:
                s.append(day["low"]["celsius"])
            return s
        except:
            return [""]

    # Method - daylist
    # Parameters - None
    # Return - s: list of strings
    # Purpose - Gets the names of the 10 days included in the forecast
    def daylist(self):
        days = []
        try:
            for day in self.data["forecast"]["txt_forecast"]["forecastday"]:
                # only days, no nights
                if day["period"] % 2 == 0:
                    days.append(day["title"])
            return days
        except:
            return [""]


