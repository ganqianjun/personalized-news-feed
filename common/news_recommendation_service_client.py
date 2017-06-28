import os
import pyjsonrpc
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'configuration'))

from config_parser import config

HOST=config['news_recommendation']['host']
PORT=config['news_recommendation']['port']
URL = "http://" + HOST + ':' + PORT

client = pyjsonrpc.HttpClient(url=URL)

def getPreferenceForUser(userId):
    preference = client.call('getPreferenceForUser', userId)
    #print "Preference list: %s" % str(preference)
    return preference
