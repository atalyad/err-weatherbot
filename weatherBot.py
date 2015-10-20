import six
from errbot import BotPlugin, botcmd
from errbot.utils import ValidationException
from itertools import chain
from six.moves.urllib.error import HTTPError
import weather
import logging
import consts

CONFIG_TEMPLATE = { consts.UNITS_CONFIG_NAME: 'metric',
                    consts.API_KEY_CONFIG_NAME: '' }

class WeatherBot(BotPlugin):
    @botcmd
    def weather(self, mess, args):
        """ Shows weather info for given location.
        Example: !weather San Francisco, CA
        or !weather brussels
        """
        if not args:
            return 'Am I supposed to guess the location?...'

        logging.debug("asking for weather. location = {}, args: {}".format(args.strip(), str(self.config)))
        return weather.get_weather_for_location(location=args.strip(),
                                                **self.config)

    def get_configuration_template(self):
        return CONFIG_TEMPLATE

    def configure(self, configuration):
        if configuration is not (None or {}):
            config = dict(chain(CONFIG_TEMPLATE.items(),
                                configuration.items()))
        else:
            config = CONFIG_TEMPLATE

        logging.debug("new config is: " + str(config))
        super(WeatherBot, self).configure(config)

    def check_configuration(self, configuration):
        units = configuration.get(consts.UNITS_CONFIG_NAME, None)
        if units and units not in ['metric', 'imperial']:
            raise ValidationException('units config has to be either metric or imperial, not: ' + units)

        api_key = configuration.get(consts.API_KEY_CONFIG_NAME, '')
        try:
            weather.perform_request(api_key=api_key)
        except HTTPError as e:
            raise ValidationException("OpenWeatherMap - " + e.read())
