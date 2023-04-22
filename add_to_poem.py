import requests
import json
import math
import os

print("Calling the OpenWeather API")

# Constants
OPEN_WEATHER_API_KEY = os.environ['OPEN_WEATHER_API_KEY']
LATITUDE = "41.890790"
LONGITUDE = "-87.581239"
OPEN_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather?lat=%s&lon=%s&appid=%s" % (LATITUDE, LONGITUDE, OPEN_WEATHER_API_KEY)
response = requests.get(OPEN_WEATHER_URL)
data = json.loads(response.text)
print(data)

print("Finished running add_to_poem.py")
