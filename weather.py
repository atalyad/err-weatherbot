import six
from six.moves.urllib.parse import quote, urlencode
from six.moves.urllib import request
from json import loads
from datetime import datetime
import logging
import consts

MESSAGE = """Found it! it looks like the forecast is '{description}'
Here's some more info:
Location: {location} at {time}
Temperature: {temp}{temp_symbol} [ low: {min_temp}{temp_symbol} \ high: {max_temp}{temp_symbol}]
Humidity: {humidity}%
Wind: {wind_direction} {speed} m/s
Pressure: {pressure}hP
"""
TEMP_SIGN = { 'metric': 'C', 'imperial': 'F' }

SUPPORTED_PARAMETERS = {
    consts.LOCATION_CONFIG_NAME: lambda l: ('q', quote(l)),
    consts.UNITS_CONFIG_NAME: lambda u: ('units', u),
    consts.API_KEY_CONFIG_NAME: lambda k: ('APPID', k)
}

def perform_request(**kwargs):
    """
    performs request with all supported parameters.
    skips unknown parameters.
    """
    args = dict([SUPPORTED_PARAMETERS[key](val) for key, val in kwargs.items() if key in SUPPORTED_PARAMETERS])
    url = consts.WEATHER_URL + urlencode(args)
    logging.debug("performing request to: {}, original args: {}".format(url, str(kwargs)))
    res = request.urlopen(url)
    decoded = loads(bytes.decode(res.read()))
    return decoded

def get_weather_for_location(location, units, **kwargs):
    """
    current supported parameters are: location, units, api_key
    """
    try:
        wm = perform_request(location=location, units=units, **kwargs)
        if wm['cod'] == 404:
            return wm['message']

        logging.debug(wm)
        p = {'location': wm['name'] + ', ' + wm['sys']['country'],
             'time' : datetime.fromtimestamp(int(wm['dt'])).strftime(consts.DATE_FMT),
             'description' :wm['weather'][0]['description'],
             'temp' : wm['main']['temp'],
             'min_temp' : wm['main']['temp_min'],
             'max_temp' : wm['main']['temp_max'],
             'humidity' : wm['main']['humidity'],
             'wind_direction' : wm['wind']['deg'],
             'speed' : wm['wind']['speed'],
             'pressure' : wm['main']['pressure'],
             'temp_symbol': TEMP_SIGN[units]
             }
        return MESSAGE.format(**p)
    except Exception as e:
        logging.exception("weatherbot crashed")
        return 'There was an error: %s' % str(e)
