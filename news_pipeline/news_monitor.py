import ast
import datetime
import hashlib
import json
import os
import redis
import sys

# because news_api_client is at anohter folder
# we could also use  '__init__.py'
# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'configuration'))

import news_api_client
from cloudAMQP_client import CloudAMQPClient
from config_parser import config

NEWS_SOURCES = ast.literal_eval(config['newspaper']['news_sources'])

REDIS_HOST = config['redis']['host']
REDIS_PORT = config['redis']['port']
NEWS_TIME_OUT_IN_SECONDS = config['redis']['expiration']

redis_client = redis.StrictRedis(REDIS_HOST, REDIS_PORT)

SCRAPE_NEWS_TASK_QUEUE_URL = config['cloudAMQP']['scrape_news_task_queue_url']
SCRAPE_NEWS_TASK_QUEUE_NAME = config['cloudAMQP']['scrape_news_task_queue_name']

scrape_news_queue_client = CloudAMQPClient(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)

SLEEP_TIME_IN_SECONDS = int(config['cloudAMQP']['scrape_news_task_queue_sleep_time_in_monitor'])

while True:
    news_list = news_api_client.getNewsFromSource(NEWS_SOURCES)
    num_of_new_news = 0

    for news in news_list:
        news_digest = hashlib.md5(news['title'].encode('utf-8')).digest().encode('base64')

        if redis_client.get(news_digest) is None:
            num_of_new_news = num_of_new_news + 1
            news['digest'] = news_digest

            # if there's no published time, set it to current UTC time
            if news['publishedAt'] is None:
                news['publishedAt'] = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

            redis_client.set(news_digest, news)
            redis_client.expire(news_digest, NEWS_TIME_OUT_IN_SECONDS)

            scrape_news_queue_client.sendMessage(news)

    print "Fetched %d news." % num_of_new_news

    scrape_news_queue_client.sleep(SLEEP_TIME_IN_SECONDS)
