import requests

# Weather4Day class uses wunderground's 4 day weather API request format, to retrieve the upcoming 4 days of weather
# forecasts.
class Weather4Day:
    # Init method makes the api call using the country and city names passed to the class, then parses the data as json
    # format.
    def __init__(self, country, city):
        url = "http://api.wunderground.com/api/034fa2c65c35e441/forecast/q/{}/{}.json".format(country, city)
        response = requests.get(url)
        self.data = response.json()

    # forecastTodayText gets the text of the current day's forecast by looping through the data given by the API until
    # the current day is found
    def forecasttodaytext(self):
        s = ""
        for day in self.data["forecast"]["txt_forecast"]["forecastday"]:
            if day["period"] == 0:
                s = day["fcttext_metric"]
        return s

    # Today's highest forecast temperature, in celsius
    def forecasttodayhigh(self):
        s = ""
        for day in self.data["forecast"]["simpleforecast"]["forecastday"]:
            if day["period"] == 1:
                s = day["high"]["celsius"]
        return s

    # Today's lowest forecast temperature, in celsius
    def forecasttodaylow(self):
        s = ""
        for day in self.data["forecast"]["simpleforecast"]["forecastday"]:
            if day["period"] == 1:
                s = day["low"]["celsius"]
        return s

    # Tomorrow's forecast, text form
    def forecasttomorrowtext(self):
        s = ""
        for day in self.data["forecast"]["txt_forecast"]["forecastday"]:
            if day["period"] == 2:
                s = day["fcttext_metric"]
        return s

    # Tomorrow's highest forecast temperature, in celsius
    def forecasttomorrowhigh(self):
        s = ""
        for day in self.data["forecast"]["simpleforecast"]["forecastday"]:
            if day["period"] == 2:
                s = day["high"]["celsius"]
        return s

    # Tomorrow's lowest forecast temperature, in celsius
    def forecasttomorrowlow(self):
        s = ""
        for day in self.data["forecast"]["simpleforecast"]["forecastday"]:
            if day["period"] == 2:
                s = day["low"]["celsius"]
        return s


# WEATHER10DAY
# Retrieves a 10-day forecast, using Wunderground's 10-day request API
class Weather10Day:
    # Uses 10 day request
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

# testing
# country = input("Enter country: ")
# city = input("Enter city: ")
# w = Weather4Day("fr", "paris")
# print(w.forecastTodayText())

