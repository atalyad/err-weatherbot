__author__ = 'AP'
from urllib import quote
import urllib2
from xml.dom import minidom

WEATHER_URL = 'http://www.google.com/ig/api?weather='


def get_weather_for_location(location):

    try:

        try:
            res = urllib2.urlopen(WEATHER_URL+ quote(location))
            dom = minidom.parseString(unicode(res.readlines()[0],  errors='ignore'))
        except :
            return 'Could not read the weather data for your location... it has funky characters in it....'

        if dom.getElementsByTagName('problem_cause'):
            return 'is that a real place?... can\'t find it... :( '

        ans = ''
        for node in dom.getElementsByTagName('forecast_information'):
             for n in node.getElementsByTagName('forecast_date'):
                ans += 'Forecast date: %s, ' % n.getAttribute('data')
             for n in node.getElementsByTagName('city'):
                 ans += (' Taken at %s' % n.getAttribute('data'))
             ans += '\n'

        i = 0
        for node in dom.getElementsByTagName('forecast_conditions'):
            if not i:
                ans += 'Today: '
            else:
                for n in node.getElementsByTagName('day_of_week'):
                    ans += n.getAttribute('data') + ': '
            for n in node.getElementsByTagName('condition'):
                ans += n.getAttribute('data') + ' '
            for n in node.getElementsByTagName('low'):
                low = int(n.getAttribute('data'))
                if low is not None:
                    ans += str(round((low - 32) / (9.0/5.0))) #convert to celsius
            for n in node.getElementsByTagName('high'):
                high = int(n.getAttribute('data'))
                if high is not None:
                    ans += ' - %s' % str(round((high - 32) / (9.0/5.0))) + u'\u2103, ' #convert to celsius
            i+= 1


        return ans.rstrip(' ,')

    except Exception,e:
        return 'There was an error: %s' % str(e)


