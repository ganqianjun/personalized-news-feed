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

for config_file_name in config_file_lists:
    # load the configuration file
    with open(os.path.join(config_file_path, config_file_name)) as f:
        config_file_load = f.read()
    config_file = ConfigParser.RawConfigParser(allow_no_value=True)
    config_file.readfp(io.BytesIO(config_file_load))

    for section in config_file.sections():
        config[section] = {}
        for options in config_file.options(section):
            config[section][options] = config_file.get(section, options)
# print config
