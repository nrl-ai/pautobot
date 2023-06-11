from weather import get_weather_data, parser, response
import streamlit as st
import spacy
from spacy.matcher import Matcher

st.title("Weather Asking")
query = st.text_input("Query: ")
if st.button("Get response"):
    model = "en_core_web_sm"
    nlp = spacy.load(model)
    doc = nlp(query)

    parse = parser.Parser(model, query)
    location = parse.get_location()
    main_topic = parse.get_maintopic()

    if location != None:
        weather = get_weather_data.WeatherAPI(location)
        data = weather.get_data()

    response = response.GenerateResponse(main_topic[0], data)
    st.write(response.get_response())






    
