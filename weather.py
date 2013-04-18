__author__ = 'AP'
from urllib import quote
import urllib2
import json
from xml.dom import minidom

WEATHER_URL = 'http://api.openweathermap.org/data/2.1/find/' # 'http://www.google.com/ig/api?weather='


def get_weather_for_location(location):

    try:

        try:
            #TODO: support config units: metric / imperial
            res = urllib2.Request(WEATHER_URL + 'name?units=metric&q=' + location)
            opener = urllib2.build_opener()
            f = opener.open(res)
            j = json.load(f)
        except Exception, e :
            print e
            return 'Could not read the weather data for your location... it has funky characters in it....'

        if 'message' in j and j['message'] == 'not found':
            return 'is that a real place?... can\'t find it... :( '

        ans = ''

        if j and 'list' in j:
            l = j['list']
            if l and l.count:
                data = l[0]

                if data and 'name' in data:
                    ans += data['name'] + ': '

                if 'main' in data and 'temp' in data['main']:
                    ans += 'Today: ' + unicode(round(data['main']['temp'])) + u'\u2103'
                    if 'temp_min' in data['main'] and 'temp_max' in data['main']:
                        ans += ' low: ' + unicode(round(data['main']['temp_min'])) + u'\u2103'
                        ans += ' high: ' + unicode(round(data['main']['temp_max'])) + u'\u2103'

                if 'weather' in data and data['weather'].count:
                    if data['weather'][0]['main']:
                        ans += ' ' + data['weather'][0]['main']
                        if data['weather'][0]['description']:
                            ans += ', ' + data['weather'][0]['description']

                if data and 'url' in data:
                    ans += '\n' + data['url']

        return ans.rstrip(' ,')

    except Exception,e:
        return 'There was an error: %s' % str(e)


