import ConfigParser
import io
import os

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

# print config
