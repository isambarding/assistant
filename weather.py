import requests


class Weather:
    def __init__(self, country, city):
        self.country = country
        self.city = city
        url = "http://api.wunderground.com/api/034fa2c65c35e441/forecast/q/" + country + "/" + city + ".json"
        response = requests.get(url)
        self.data = response.json()

    # Four day forecast
    def fourdays(self):
        s = ""
        for day in self.data["forecast"]["txt_forecast"]["forecastday"]:
            s = s + day["title"] + ": " + day["fcttext_metric"] + "\n"
        return (s)

    # Tomorrow's forecast
    def tomorrow(self):
        s = ""
        for day in self.data["forecast"]["txt_forecast"]["forecastday"]:
            if day["period"] == 2:
                s = s + day["title"] + ": " + day["fcttext_metric"] + "\n"
            if day["period"] == 3:
                s = s + day["title"] + ": " + day["fcttext_metric"] + "\n"
        return (s)


# testing
country = input("Enter country: ")
city = input("Enter city: ")
w = Weather(country, city)
print(w.tomorrow())

