__author__ = 'AP'

from urllib.parse import quote
import urllib.request
import logging
from json import loads
from datetime import datetime

WEATHER_URL = 'http://api.openweathermap.org/data/2.5/weather?units=metric&q='
MESSAGE = """Location {location} at {time}.
{description}
Temperature {temp} [{min_temp}-{max_temp}]
Humidity {humidity} %
Wind {wind_direction} {speed} m/s
Pressure {pressure} hP
"""
DATE_FMT = '%Y-%m-%d %H:%M:%S'
def get_weather_for_location(location):

    try:
        res = urllib.request.urlopen(WEATHER_URL + quote(location))
        wm = loads(bytes.decode(res.read()))
        logging.debug(wm)
        p = {'location': wm['name'] + ', ' + wm['sys']['country'],
             'time' : datetime.fromtimestamp(int(wm['dt'])).strftime(DATE_FMT),
             'description' :wm['weather'][0]['description'],
             'temp' : wm['main']['temp'],
             'min_temp' : wm['main']['temp_min'],
             'max_temp' : wm['main']['temp_max'],
             'humidity' : wm['main']['humidity'],
             'wind_direction' : wm['wind']['deg'],
             'speed' :wm['wind']['speed'],
             'pressure' : wm['main']['pressure'],
             }
        return MESSAGE.format(**p)
    except Exception as e:
        logging.exception("weather crashed")
        return 'There was an error: %s' % str(e)


