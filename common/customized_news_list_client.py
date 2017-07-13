import os
import pyjsonrpc
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'configuration'))

from config_parser import config
from sys_log_client import logger

HOST = str(config['customized_news_list']['host'])
PORT = str(config['customized_news_list']['port'])
URL = 'http://' + HOST + ':' + PORT

client = pyjsonrpc.HttpClient(url=URL)

def predict_news_click(user_id, news_description):
    click_predict = client.call('predict_news_click', user_id, news_description)
    return click_predict
