__author__ = 'AP'
import urllib2
from xml.dom import minidom

WEATHER_URL = 'http://www.google.com/ig/api?weather='

def get_weather_for_location(location):

    try:

        try:
            dom = minidom.parse(urllib2.urlopen(WEATHER_URL+location))
        except :
            return 'Could not read the weather data for your location... it has funky characters in it....'

        if dom.getElementsByTagName('problem_cause'):
            return 'is that a real place?... can\'t find it... :( '

        ans = '\n Weather forecast for %s \n\n' % location
        for node in dom.getElementsByTagName('forecast_information'):
             for n in node.getElementsByTagName('forecast_date'):
                ans += 'Forecast date: %s, ' % n.getAttribute('data')
             for n in node.getElementsByTagName('city'):
                 ans += (' Taken at %s' % n.getAttribute('data'))
             for n in node.getElementsByTagName('current_date_time'):
                 ans += ' on %s' % n.getAttribute('data')
             ans += '\n\n'

        for node in dom.getElementsByTagName('current_conditions'):
            ans += '*Current conditions*: \n'
            for n in node.getElementsByTagName('condition'):
                ans += 'Condition: %s\n' % n.getAttribute('data')
            for n in node.getElementsByTagName('temp_c'):
                ans += 'Temps: %s c\n' % n.getAttribute('data')
            for n in node.getElementsByTagName('humidity'):
                ans += '%s\n' % n.getAttribute('data')
            for n in node.getElementsByTagName('wind_condition'):
                ans += '%s\n\n' % n.getAttribute('data')


        ans += '*Forecast conditions*: \n\n'
        for node in dom.getElementsByTagName('forecast_conditions'):
            for n in node.getElementsByTagName('day_of_week'):
                ans += 'Day of week: %s\n' % n.getAttribute('data')
            for n in node.getElementsByTagName('condition'):
                ans += '%s\n' % n.getAttribute('data')
            for n in node.getElementsByTagName('low'):
                low = int(n.getAttribute('data'))
                if low is not None:
                    ans += 'Low: %s c\n' % str(round((low - 32) / (9.0/5.0))) #convert to celsius
            for n in node.getElementsByTagName('high'):
                high = int(n.getAttribute('data'))
                if high is not None:
                    ans += 'high %s c\n\n' % str(round((high - 32) / (9.0/5.0))) #convert to celsius


        return ans

    except Exception,e:
        return 'There was an error: %s' % str(e)


