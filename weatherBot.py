from weather import get_weather_for_location
from errbot import BotPlugin, botcmd

__author__ = 'AP'


class WeatherBot(BotPlugin):

    @botcmd
    def weather(self, mess, args):
        """ Shows weather info for given location.
        Example: !weather San Francisco, CA
        or !weather brussels
        """
        if not args:
            return 'Am I supposed to guess the location?...'
        return get_weather_for_location(args.strip())

