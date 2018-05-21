import requests

# WEATHER.PY
# Contains classes for retrieving a 4-day or 10-day forecast.
# USAGE: Country can be full name ("France") or as 2 letter country code ("FR")
# Note that the 2 letter country code is NOT the ISO code- Wunderground uses its own system
# City must be full name ("Paris")
# 21/05/18: tested working

# WEATHER4DAY
# Retrieves a 4-day forecast, using Wunderground's 4-day request API
class Weather4Day:
    # Uses 4 day request
    def __init__(self, country, city):
        url = "http://api.wunderground.com/api/034fa2c65c35e441/forecast/q/" + country + "/" + city + ".json"
        response = requests.get(url)
        self.data = response.json()

    # Today's forecast, in text
    def forecastTodayText(self):
        s = ""
        for day in self.data["forecast"]["txt_forecast"]["forecastday"]:
            if day["period"] == 0:
                s = day["fcttext_metric"]
        return s

    # Today's highest forecast temperature, in celsius
    def forecastTodayHigh(self):
        s = ""
        for day in self.data["forecast"]["simpleforecast"]["forecastday"]:
            if day["period"] == 1:
                s = day["high"]["celsius"]
        return s

    # Today's lowest forecast temperature, in celsius
    def forecastTodayLow(self):
        s = ""
        for day in self.data["forecast"]["simpleforecast"]["forecastday"]:
            if day["period"] == 1:
                s = day["low"]["celsius"]
        return s

    # Tomorrow's forecast, text form
    def forecastTomorrowText(self):
        s = ""
        for day in self.data["forecast"]["txt_forecast"]["forecastday"]:
            if day["period"] == 2:
                s = day["fcttext_metric"]
        return s

    # Tomorrow's highest forecast temperature, in celsius
    def forecastTomorrowHigh(self):
        s = ""
        for day in self.data["forecast"]["simpleforecast"]["forecastday"]:
            if day["period"] == 2:
                s = day["high"]["celsius"]
        return s

    # Tomorrow's lowest forecast temperature, in celsius
    def forecastTomorrowLow(self):
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
        url = "http://api.wunderground.com/api/034fa2c65c35e441/forecast10day/q/" + country + "/" + city + ".json"
        response = requests.get(url)
        self.data = response.json()

    # 10 day forecast, text version
    def forecast10DaysText(self):
        s = []
        for day in self.data["forecast"]["txt_forecast"]["forecastday"]:
            # Only days, not nights
            if day["period"] % 2 == 0:
                s.append(day["fcttext_metric"])
        return s

    # Highest forecast temperature of next 10 days, in celsius
    def forecast10DaysHigh(self):
        s = []
        for day in self.data["forecast"]["simpleforecast"]["forecastday"]:
            s.append(day["high"]["celsius"])
        return s

    # Lowest forecast temperature of next 10 days, in celsius
    def forecast10DaysLow(self):
        s = []
        for day in self.data["forecast"]["simpleforecast"]["forecastday"]:
            s.append(day["low"]["celsius"])
        return s

    def dayList(self):
        s = []
        for day in self.data["forecast"]["txt_forecast"]["forecastday"]:
            # only days, no nights
            if day["period"] % 2 == 0:
                s.append(day["title"])
        return s

# testing
#country = input("Enter country: ")
#city = input("Enter city: ")
w = Weather4Day("fr", "paris")
print(w.forecastTodayText())

