from urllib2 import urlopen
import json
import RPi.GPIO as gpio
from time import strftime
from time import localtime

#setup the GPIO pins
gpio.setmode(gpio.BCM)
gpio.setwarnings(False)
gpio.setup(18, gpio.OUT)


#function to get the latest weather status
def getWeatherStatus():
        weather = urlopen('http://api.wunderground.com/api/{your_weather_api_key}/astronomy/q/{your_city}/{your_city}.json')
        json_string = weather.read()
        return json.loads(json_string)

#function to get the time for sunset
def getSunset(weatherStatus):
        sunsetHour = weatherStatus['moon_phase']['sunset']['hour']
        sunsetMinute = weatherStatus['moon_phase']['sunset']['minute']
        return sunsetHour + sunsetMinute


#function to update the sunset time
def updateSunsetTime():
        newWeatherData = getWeatherStatus()
        return getSunset(newWeatherData)
        
        

#initial values
weatherData = getWeatherStatus()
sunSet = getSunset(weatherData)

lateNight = "2300"
isLampOn = False
counter = 0


#start up program
while True:
        
        currentTime = strftime("%H%M", localtime())
                
        if isLampOn:
                if currentTime > lateNight:
                        gpio.output(18, gpio.LOW)
                        isLampOn = False
                        counter = counter + 1
        else:
                if currentTime > sunSet and currentTime < lateNight:
                        gpio.output(18, gpio.HIGH)
                        isLampOn = True

        if counter > 2:
                sunSet = updateSunsetTime()
                counter = 0  
