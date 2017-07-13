import os
import sys

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'configuration'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'monitor_service'))

import mongodb_client
from config_parser import config
from graphite_client import graphite
from news_list_training_data_generator import training_data_generator
from sys_log_client import logger

CLICK_LOGS_TABLE_NAME = str(config['mongodb']['table_clicks'])
NEWS_TABLE_NAME = str(config['mongodb']['table_news'])

db = mongodb_client.get_db()

user_list = db[CLICK_LOGS_TABLE_NAME].distinct("userId")
logger.debug("Customized - user_list:\n %s " % (', '.join(user for user in user_list)))

training_data_generator.export_training_data(user_list)
