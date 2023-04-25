import requests
import json
import math
import random
import os
from pathlib import Path
from jinja2 import FileSystemLoader, Environment

# Constants
OPEN_WEATHER_API_KEY = os.environ['OPEN_WEATHER_API_KEY']
LATITUDE = "41.890790"
LONGITUDE = "-87.581239"
OPEN_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather?lat=%s&lon=%s&appid=%s&units=imperial" % (LATITUDE, LONGITUDE, OPEN_WEATHER_API_KEY)

# Call OpenWeather API
response = requests.get(OPEN_WEATHER_URL)
data = json.loads(response.text)
print("Response from the OpenWeather API:")
print(data)

# Pull out the specific weather stats we want to use
temp = data["main"]["temp"]
print("temp="+str(temp))
windSpeed = data["wind"]["speed"]
print("windSpeed="+str(windSpeed))
windDir = data["wind"]["deg"]
print("windDir="+str(windDir))

# Load the existing stats
statsStr = Path('stats.json').read_text()
stats = json.loads(statsStr)
balance = stats["balance"]
mood = stats["mood"]

# Load the word files
moodsStr = Path("moods.json").read_text()
moods = json.loads(moodsStr)

# Generate poem text based on stats and weather params
newLine = ""
if temp > stats["temp"]:
    mood += 1
    newLine += "you get angrier, "
    newLine += moods["very_angry"][random.randint(0, len(moods["very_angry"]))]+", "
else:
    mood -= 1
    newLine += "you get calmer, "
    newLine += moods["calm"][random.randint(0, len(moods["calm"]))]+", "
if windDir > 180:
    balance += 1
    newLine += "you advance, "
else:
    balance -= 1
    newLine += "your opponent advances, "
if balance > 0:
    newLine += "you are winning, "
else:
    newLine += "your opponent is winning, "

print("New line is: " + newLine)

# Update the stats file with the new stats
stats["balance"] = balance
stats["mood"] = mood
stats["temp"] = temp
Path("stats.json").write_text(json.dumps(stats))

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
