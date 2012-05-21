from botplugin import BotPlugin
from weather import get_weather_for_location

__author__ = 'AP'

from jabberbot import botcmd

class WeatherBot(BotPlugin):

    @botcmd
    def weather(self, mess, args):
        """ Shows weather info for given location. Example: !weather New-York,NY """
        if not args:
            return 'Am I supposed to guess the location?...'
        args = args.strip()
        return get_weather_for_location(args)

