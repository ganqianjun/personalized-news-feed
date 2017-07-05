import ConfigParser
import os
import sys

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
from sys_log_client import logger

config = {}

config_file_path = os.path.dirname(__file__)
config_file_lists = [
  'config_common.ini',
  'config_service.ini',
  'config_news_topics.ini'
]

config_parser = ConfigParser.RawConfigParser(allow_no_value=True)
for config_file in config_file_lists:
    config_parser.read(os.path.join(config_file_path, config_file))

for section in config_parser.sections():
    config[section] = {}
    for options in config_parser.options(section):
        config[section][options] = config_parser.get(section, options)

logger.debug("The configuration is: ")
logger.debug(config)
