import logging
import io
import os

from logging.handlers import RotatingFileHandler

#create logger
logger = logging.getLogger('news_feed')
logger.setLevel(logging.INFO)

log_file_path = os.path.dirname(__file__)

log_file_name = 'system_log.log'

logHandler = RotatingFileHandler(os.path.join(log_file_path, log_file_name), mode='a', maxBytes=0, backupCount=0, encoding=None, delay=0)
logHandler.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
logHandler.setFormatter(formatter)

# add ch to logger
logger.addHandler(logHandler)
