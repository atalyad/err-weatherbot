from weather import get_weather_for_location

# Backward compatibility
from errbot.version import VERSION
from errbot.utils import version2array
if version2array(VERSION) >= [1,6,0]:
    from errbot import botcmd, BotPlugin
else:
    from errbot.botplugin import BotPlugin
    from errbot.jabberbot import botcmd


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

