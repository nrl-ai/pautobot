import pywttr

class WeatherAPI():
    def __init__(self, location):
        self.location = location
    
    def get_data(self):
        data = pywttr.Wttr(self.location)
        data = data.en()
        get_data = data.dict(exclude_defaults=True)

        return {
                    "current_condition": {
                        "Location" : get_data["nearest_area"][0]["area_name"][0]["value"],
                        "Describe" : get_data["current_condition"][0]["weather_desc"][0]["value"].lower(),
                        "Temperature" : get_data["current_condition"][0]["temp_c"],
                        "Humidity" : get_data["current_condition"][0]["humidity"],
                        "Wind_speed" : get_data["current_condition"][0]["windspeed_kmph"]
                    }
                }