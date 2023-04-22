import requests
import json
import math
import os
from pathlib import Path
from jinja2 import FileSystemLoader, Environment

print("Calling the OpenWeather API")

# Constants
OPEN_WEATHER_API_KEY = os.environ['OPEN_WEATHER_API_KEY']
LATITUDE = "41.890790"
LONGITUDE = "-87.581239"
OPEN_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather?lat=%s&lon=%s&appid=%s" % (LATITUDE, LONGITUDE, OPEN_WEATHER_API_KEY)

# Call OpenWeather API
response = requests.get(OPEN_WEATHER_URL)
data = json.loads(response.text)
print(data)

# Pull out the specific weather stats we want to use
weather = data["weather"][0]["main"]
dt = data["dt"]

print("weather="+weather)
print("dt="+dt)

# Build an html file based on the output we've generated
loader = FileSystemLoader(".")
env = Environment(
    loader=loader, extensions=["jinja2_humanize_extension.HumanizeExtension"]
)
template = env.get_template("index.jinja")
Path("index.html").write_text(
    template.render(
        {
            "weather" : weather,
            "date" : dt
        }
    )
)

print("Generated index.html")

print("Finished running add_to_poem.py")
