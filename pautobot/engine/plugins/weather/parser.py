import spacy
from spacy.matcher import Matcher

class Parser():
    def __init__(self, model, query):
        self.model_name = model
        self.nlp = spacy.load(self.model_name)
        self.query = query
        self.doc = self.nlp(query)
        self.matcher = Matcher(self.nlp.vocab)
    
    def get_location(self):
        location = [ent.text for ent in self.doc.ents if ent.label_ == "GPE"]
        return location

    def get_maintopic(self):
        weather_pattern = [{'LOWER': 'weather'}]
        temperature_pattern = [{'LOWER': 'temperature'}]
        humidity_pattern = [{'LOWER': 'humidity'}]
        windspeed_pattern = [{'LOWER': 'wind speed'}]

        # Add patterns to the matcher
        self.matcher.add('WEATHER', [weather_pattern])
        self.matcher.add('TEMPERATURE', [temperature_pattern])
        self.matcher.add('HUMIDITY', [humidity_pattern])
        self.matcher.add('WINDSPEED', [windspeed_pattern])

        # Extract weather and temperature matches
        weather = None
        temperature = None
        humidity = None
        wind_speed = None

        matches = self.matcher(self.doc)
        main_topic = []

        for match_id, start, end in matches:
            match_text = self.doc[start:end].text.lower()
            if match_text == 'weather':
                weather = match_text
                main_topic.append(weather)
            elif match_text == 'temperature':
                temperature = match_text
                main_topic.append(temperature)
            elif match_text == 'humidity':
                humidity = match_text
                main_topic.append(humidity)
            elif match_text == 'wind speed':
                wind_speed = match_text
                main_topic.append(wind_speed)
            
        return main_topic
