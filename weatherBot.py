from errbot.botplugin import BotPlugin
from errbot.jabberbot import botcmd
from weather import get_weather_for_location

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
        args = args.strip()
        return get_weather_for_location(args)

