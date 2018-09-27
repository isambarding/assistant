import requests


class Weather4Day:
    # Method - Weather4Day init
    # Parameters - country: string, city: string
    # Return - None
    # Purpose - Makes an api call  for the next 4 days of weather using the country and city arguments, then parses the
    #           data as json format.
    def __init__(self, country, city):
        url = "http://api.wunderground.com/api/034fa2c65c35e441/forecast/q/{}/{}.json".format(country, city)
        response = requests.get(url)
        self.data = response.json()

    # Method - forecasttodaytext
    # Parameters - None
    # Return - s: string
    # Purpose - Gets the text forecast for the current day
    def forecasttodaytext(self):
        for day in self.data["forecast"]["txt_forecast"]["forecastday"]:
            if day["period"] == 0:
                s = day["fcttext_metric"]
        return s

    # Method - forecasttodayhigh
    # Parameters - None
    # Return - s: string
    # Purpose - Gets the highest forecast temperature for the current day
    def forecasttodayhigh(self):
        for day in self.data["forecast"]["simpleforecast"]["forecastday"]:
            if day["period"] == 1:
                s = day["high"]["celsius"]
        return s

    # Method - forecasttodaylow
    # Parameters - None
    # Return - s: string
    # Purpose - Gets the highest forecast temperature for the current day
    def forecasttodaylow(self):
        for day in self.data["forecast"]["simpleforecast"]["forecastday"]:
            if day["period"] == 1:
                s = day["low"]["celsius"]
        return s

    # Method - forecasttomorrowtext
    # Parameters - None
    # Return - s: string
    # Purpose - Gets the text forecast for the following day
    def forecasttomorrowtext(self):
        for day in self.data["forecast"]["txt_forecast"]["forecastday"]:
            if day["period"] == 2:
                s = day["fcttext_metric"]
        return s

    # Method - forecasttomorrowhigh
    # Parameters - None
    # Return - s: string
    # Purpose - Gets the highest forecast temperature for the following day
    def forecasttomorrowhigh(self):
        for day in self.data["forecast"]["simpleforecast"]["forecastday"]:
            if day["period"] == 2:
                s = day["high"]["celsius"]
        return s

    # Method - forecasttomorrowlow
    # Parameters - None
    # Return - s: string
    # Purpose - Gets the lowest forecast temperature for the following day
    def forecasttomorrowlow(self):
        for day in self.data["forecast"]["simpleforecast"]["forecastday"]:
            if day["period"] == 2:
                s = day["low"]["celsius"]
        return s


class Weather10Day:
    # Method - Weather10Day init
    # Parameters - country: string, city: string
    # Return - None
    # Purpose - Makes an api call  for the next 10 days of weather using the country and city arguments, then parses the
    #           data as json format.
    def __init__(self, country, city):
        url = "http://api.wunderground.com/api/034fa2c65c35e441/forecast10day/q/{}/{}.json".format(country, city)
        response = requests.get(url)
        self.data = response.json()

    # 10 day forecast, text version
    def forecast10daystext(self):
        s = []
        for day in self.data["forecast"]["txt_forecast"]["forecastday"]:
            # Only days, not nights
            if day["period"] % 2 == 0:
                s.append(day["fcttext_metric"])
        return s

    # Highest forecast temperature of next 10 days, in celsius
    def forecast10dayshigh(self):
        s = []
        for day in self.data["forecast"]["simpleforecast"]["forecastday"]:
            s.append(day["high"]["celsius"])
        return s

    # Lowest forecast temperature of next 10 days, in celsius
    def forecast10dayslow(self):
        s = []
        for day in self.data["forecast"]["simpleforecast"]["forecastday"]:
            s.append(day["low"]["celsius"])
        return s

    def daylist(self):
        s = []
        for day in self.data["forecast"]["txt_forecast"]["forecastday"]:
            # only days, no nights
            if day["period"] % 2 == 0:
                s.append(day["title"])
        return s


