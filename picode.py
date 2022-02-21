import sys
import bs4
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import os
import sys
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106
from luma.core.virtual import viewport
import time
import datetime
import wolframalpha
import speech_recognition as sr
import pyaudio
import wikipedia
from picamera import PiCamera
import python_weather
import asyncio
import dropbox
import picamera
from twilio.rest import Client
import requests
import json
import math

bad_chars = [';', '|', '(', ')', '+', '=', '1']


def listen():

  listening_screen()

  sound = sr.Recognizer()

  with sr.Microphone() as audio:
    said = sound.listen(audio)
  try:

    global val
    val = sound.recognize_google(said, language = 'en-GB', show_all = False)
    print(val)

    say(str(val))
    return(val)
  except sr.UnknownValueError:
    print("Could not understasnd, Please repeat")



def say(statment):
  statment1 = statment.replace(" ", "_")
  os.system('espeak ' + str(statment1) + ' -ven+m1 -k5 -g4 -s120')



def start_up():
  hour1 = int(datetime.datetime.now().hour)
  if hour1 >= 0 and hour1 < 5:
      say('go_to_sleep')
  if hour1 >= 5 and hour1 < 12:
      say('good_morning')
  elif hour1 >= 12 and hour1 < 20:
      say('good_afternoon')
  else:
      say('good_evening')


async def getweather():
    client = python_weather.Client(format=python_weather.METRIC)
    weather = await client.find("London")
    t = weather.current.temperature
    y = weather.current.sky_text
    if len(y) > 6:
      x = y.split()
      x1 = x[0]
      x2 = x[1]
      x1 = x1[:2]
      x2 = x2[:3]
      y = (str(x1) + " " + str(x2))
    else:
	    y = y
    await client.close()
    return(t, y)

async def getweatherlong():
    client = python_weather.Client(format=python_weather.METRIC)
    weather = await client.find("London")
    t = weather.current.temperature
    s = weather.current.sky_text
    h = weather.current.humidity
    w = weather.current.wind_speed
      
    await client.close()
    return(t, s, h, w)

def front_screen():
  cdt = datetime.datetime.now()
  min1 = str(cdt.minute)
  hour = str(cdt.hour)
  day = str(cdt.day)
  month = str(cdt.month)

  with canvas(device) as draw:
    if int(hour) < 10:
      draw.text((0,0), "0" + hour, fill = "blue")
    else:
      draw.text((0, 0), hour, fill = "blue")
    draw.text((11, 0),":", fill = "blue")
    if int(min1) < 10:
        draw.text((15, 0), "0" + min1, fill = "blue")
    else:
        draw.text((15, 0), min1, fill = "blue")
    draw.text((0, 10), "___________", fill = "yellow")
    #draw.text((0, 9), date, fill = "white")
    weathertemp = "null"
    weathersky = "null"
    if 1 == 1:
        loop = asyncio.get_event_loop()
        weathertemp, weathersky = loop.run_until_complete(getweather())    
    
    draw.text((33, 0), str(weathertemp) + "°C", fill = "red")
    draw.text((28, 9), str(weathersky), fill = "white")
    draw.text((0, 9), day + "/" + month, fill = "blue")

def listening_screen():
  cdt = datetime.datetime.now()
  min1 = str(cdt.minute)
  hour = str(cdt.hour)
  day = str(cdt.day)
  month = str(cdt.month)

  with canvas(device) as draw:
    if int(hour) < 10:
      draw.text((0,0), "0" + hour, fill = "blue")
    else:
      draw.text((0, 0), hour, fill = "blue")
    draw.text((11, 0),":", fill = "blue")
    if int(min1) < 10:
        draw.text((15, 0), "0" + min1, fill = "blue")
    else:
        draw.text((15, 0), min1, fill = "blue")
    draw.text((0, 10), "___________", fill = "yellow")
    #draw.text((0, 9), date, fill = "white")
    weathertemp = "null"
    weathersky = "null"
    if 1 == 1:
        loop = asyncio.get_event_loop()
        weathertemp, weathersky = loop.run_until_complete(getweather())    
    
    draw.text((33, 0), str(weathertemp) + "°C", fill = "red")
    draw.text((28, 9), str(weathersky), fill = "white")
    draw.text((0, 9), day + "/" + month, fill = "blue")
    draw.text((0, 115), "...", fill = "white")

def weather_screen():
  cdt = datetime.datetime.now()
  min1 = str(cdt.minute)
  hour = str(cdt.hour)
  day = str(cdt.day)
  month = str(cdt.month)

  with canvas(device) as draw:
    if int(hour) < 10:
      draw.text((0,0), "0" + hour, fill = "blue")
    else:
      draw.text((0, 0), hour, fill = "blue")
    draw.text((11, 0),":", fill = "blue")
    if int(min1) < 10:
        draw.text((15, 0), "0" + min1, fill = "blue")
    else:
        draw.text((15, 0), min1, fill = "blue")
    draw.text((0, 10), "___________", fill = "yellow")
    #draw.text((0, 9), date, fill = "white")
    weathertemp = "null"
    weathersky = "null"
    if 1 == 1:
        loop = asyncio.get_event_loop()
        weathertemp, weathersky, weatherhumidity, weatherwind = loop.run_until_complete(getweatherlong())    
    
    draw.text((0, 10), day + "/" + month, fill = "blue")
    draw.text((0, 20), "temp: " + str(weathertemp) + "°C", fill = "red")
    draw.text((0, 30), str(weathersky), fill = "white")
    draw.text((0, 40), "rh: " + str(weatherhumidity) + "mgL", fill = "blue")  
    draw.text((0, 50), "wind: " + str(weatherwind) + " kn", fill = "blue")


def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

def newsapi():
    response = requests.get('https://newsapi.org/v2/top-headlines?country=gb&category=technology&apiKey=94697f6d736a4ab09ca388ffeb0ac08f')
    print(response.status_code)
    articles = response.json()['articles']

    content = []
    count = 0
    for d in articles:
        writing = d["title"]
        content.append(writing)
        if(count == 5):
            return(content)
        else:
            count = count + 1

    print(content)
    #jprint(articles)

def news():
  content = newsapi()
  content1 = content[0]
  content2 = content[1]
  content3 = content[2]
  content4 = content[3]
  content5 = content[4]
  say(content1)
  say(content2)
  say(content3)
  say(content4)
  say(content5)


def weather():
  weather_screen()
  getweatherlong()
  if 1 == 1:
        loop = asyncio.get_event_loop()
        weathertemp, weathersky, weatherhumidity, weatherwind = loop.run_until_complete(getweatherlong())    

  say("The temperature is" + str(weathertemp))
  say("The sky is " + str(weathersky))
  say("Humidity is " + str(weatherhumidity))
  say("The wind speed is " + str(weatherwind))

def hacker():
  virtual = viewport(device, width=device.width, height=768)


  with open('hackerfile.txt') as f:
      contents = f.read()
      print(contents)
  f.close()

  for _ in range(2):
      with canvas(virtual) as draw:
          for i, line in enumerate(contents.split("\n")):
              draw.text((0, 40 + (i * 12)), text=line, fill="white")

  # update the viewport one position below, causing a refresh,
  # giving a rolling up scroll effect when done repeatedly
  for y in range(450):
      virtual.set_position((0, y))
      time.sleep(0.001)


def posn(angle, arm_length):
    dx = int(math.cos(math.radians(angle)) * arm_length)
    dy = int(math.sin(math.radians(angle)) * arm_length)
    return (dx, dy)


def posn(angle, arm_length):
    dx = int(math.cos(math.radians(angle)) * arm_length)
    dy = int(math.sin(math.radians(angle)) * arm_length)
    return (dx, dy)


def timefunction():
    today_last_time = "Unknown"
    timecount = 0
    while timecount < 100:
        now = datetime.datetime.now()
        today_time = now.strftime("%H:%M:%S")
        if today_time != today_last_time:
            today_last_time = today_time
            with canvas(device) as draw:
                
                now = datetime.datetime.now()

                margin = 5

                cx = 30
                cy = 32

                left = cx - cy
                right = cx + cy

                hrs_angle = 270 + (30 * (now.hour + (now.minute / 60.0)))
                hrs = posn(hrs_angle, cy - margin - 7)

                min_angle = 270 + (6 * now.minute)
                mins = posn(min_angle, cy - margin - 2)

                sec_angle = 270 + (6 * now.second)
                secs = posn(sec_angle, cy - margin - 2)

                draw.ellipse((left + margin, 50, right - margin, 50+ min(device.height, 64) - margin), outline="white")
                draw.line((cx, 50 + cy, cx + hrs[0], 50 + cy + hrs[1]), fill="white")
                draw.line((cx, 50 + cy, cx + mins[0], 50 + cy + mins[1]), fill="white")
                draw.line((cx, 50 + cy, cx + secs[0], 50 + cy + secs[1]), fill="red")
                draw.ellipse((cx - 2, 50 + cy - 2, cx + 2, 50 + cy + 2), fill="white", outline="white")

        time.sleep(0.1)
        timecount = timecount + 1

#device info
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, rotate=1)

#startup
start_up()

#loop
while True:
  front_screen()
  listen()
  try:
    if len(val) >= 2:
      if 'news' in val:
        del val
        news()
      if 'weather' in val:
        del val
        weather()
        time.sleep(5)
      if 'time' in val:
        del val
        timefunction()
        time.sleep(5)
      if 'hacker' in val:
        del val
        hacker()
        time.sleep(5)
      
      else:
        query = str(val)
        result = wikipedia.summary(val, sentences = 1)
        for i in bad_chars:
          result = result.replace(i, '')
        say(result)
        del val
        #break
      time.sleep()
  
  except:
    print(' ')
