import requests
import json
import math
import os
from pathlib import Path
from jinja2 import FileSystemLoader, Environment

# Constants
OPEN_WEATHER_API_KEY = os.environ['OPEN_WEATHER_API_KEY']
LATITUDE = "41.890790"
LONGITUDE = "-87.581239"
OPEN_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather?lat=%s&lon=%s&appid=%s" % (LATITUDE, LONGITUDE, OPEN_WEATHER_API_KEY)

# Call OpenWeather API
response = requests.get(OPEN_WEATHER_URL)
data = json.loads(response.text)
print("Response from the OpenWeather API:")
print(data)

# Pull out the specific weather stats we want to use
weather = data["weather"][0]["main"]
print("weather="+weather)

# Construct the new poem line
newLine = weather
print("New line is: " + newLine)

# Add the new poem line to the existing poem lines from the repo
prevPoemLines = Path('poem_lines.txt').read_text()
poem = prevPoemLines + "<br>" + newLine
Path("poem_lines.txt").write_text(poem)
print("Updated poem_lines.txt")

# Build an html file populated with the poem we've generated
loader = FileSystemLoader(".")
env = Environment(
    loader=loader, extensions=["jinja2_humanize_extension.HumanizeExtension"]
)
template = env.get_template("index.jinja")
Path("index.html").write_text(
    template.render(
        {
            "poem" : poem
        }
    )
)
print("Generated index.html")
