import os
import pyjsonrpc
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'configuration'))

from config_parser import config

HOST = str(config['news_topic_modeling']['host'])
PORT = str(config['news_topic_modeling']['port'])
URL = 'http://' + HOST + ':' + PORT

client = pyjsonrpc.HttpClient(url=URL)

def classify(text):
    topic = client.call('classify', text)
    #print "Topic: %s" % str(topic)
    return topic
