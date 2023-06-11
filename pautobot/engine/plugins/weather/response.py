class GenerateResponse():
    def __init__(self, topic, data):
        self.topic = topic
        self.data = data

    def get_response(self):
        if self.topic == None:
            return "Having trouble while trying to grasp the idea behind the sentences."
        elif self.topic == "weather":
            return f"The current weather in {self.data['current_condition']['Location']} is experiencing {self.data['current_condition']['Describe']}. The temperature is around {self.data['current_condition']['Temperature']}°C. The humidity level is {self.data['current_condition']['Humidity']}%. Additionally, the wind speed is approximately {self.data['current_condition']['Wind_speed']}km/h."
        elif self.topic == "temperature":
            return f"The current temperature is {self.data['current_condition']['Temperature']}°C"
        elif self.topic == "humidity":
            return f"The current humidity level is {self.data['current_condition']['Humidity']}%"
        elif self.topic == "speed":
            return f"The current wind speed is {self.data['current_condition']['Wind_speed']}km/h"
        
        